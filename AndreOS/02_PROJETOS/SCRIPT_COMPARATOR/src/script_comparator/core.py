"""Core engine for safe comparison and consolidation of script versions.

No GUI, Qt, web framework or project-specific dependency is required.
Standard library only.
"""
from __future__ import annotations

import ast
import difflib
import json
import re
import shutil
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional

FINAL_MARKERS = ("_final", "-final", "_latest", "-latest", "_complete", "-complete")
VERSION_RE = re.compile(r"(?i)(?:[_\-. ]?v?\d+)$")
SUPPORTED_TEXT_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".json", ".jsonc", ".css", ".scss",
    ".html", ".htm", ".kt", ".kts", ".java", ".cs", ".c", ".h", ".cpp",
    ".hpp", ".xml", ".yaml", ".yml", ".md", ".txt", ".sql", ".sh", ".bat",
    ".ps1", ".toml", ".ini", ".cfg", ".vue", ".svelte",
}

@dataclass
class FileInfo:
    path: Path
    base_name: str
    extension: str
    canonical_base: str
    encoding: str
    syntax_valid: Optional[bool]
    lines: int
    nonempty_lines: int
    symbols: list[str] = field(default_factory=list)
    score: float = 0.0

@dataclass
class Conflict:
    kind: str
    symbol: str
    base_file: str
    other_file: str
    detail: str

@dataclass
class MergeResult:
    group: str
    base_file: str
    output_file: Optional[str]
    changed: bool
    validated: bool
    added_symbols: list[str] = field(default_factory=list)
    added_chunks: int = 0
    conflicts: list[Conflict] = field(default_factory=list)
    backup_dir: Optional[str] = None
    warnings: list[str] = field(default_factory=list)


REPORT_SCHEMA_VERSION = "1.0"


@dataclass
class PreviewResult:
    group: str
    base_file: str
    files: list[str]
    final_file: str
    planned_original_names: list[str]
    strategy: str
    changed: bool
    validated: bool
    added_symbols: list[str] = field(default_factory=list)
    added_chunks: int = 0
    conflicts: list[Conflict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    safe_to_consolidate: bool = False


def read_text(path: str | Path) -> tuple[str, str]:
    data = Path(path).read_bytes()
    for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Unsupported text encoding: {path}")


def canonical_base(name: str | Path) -> str:
    stem = Path(name).stem
    low = stem.lower()
    for marker in FINAL_MARKERS:
        if low.endswith(marker):
            stem = stem[:-len(marker)]
            break
    stem = VERSION_RE.sub("", stem)
    stem = re.sub(r"[_\-. ]+$", "", stem)
    return stem or Path(name).stem


def group_key(path: str | Path) -> tuple[str, str]:
    p = Path(path)
    return canonical_base(p.name).casefold(), p.suffix.lower()


def group_files(paths: Iterable[str | Path]) -> dict[tuple[str, str], list[Path]]:
    result: dict[tuple[str, str], list[Path]] = {}
    for raw in paths:
        p = Path(raw)
        result.setdefault(group_key(p), []).append(p)
    return result


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def _python_symbols(text: str) -> tuple[list[str], bool]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return [], False
    symbols: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            symbols.append(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            symbols.append("import")
    return list(dict.fromkeys(symbols)), True


def _generic_symbols(text: str) -> tuple[list[str], Optional[bool]]:
    patterns = (
        r"(?m)^\s*(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_$][\w$]*)",
        r"(?m)^\s*(?:export\s+)?class\s+([A-Za-z_$][\w$]*)",
        r"(?m)^\s*(?:fun|def)\s+([A-Za-z_]\w*)",
        r"(?m)^\s*([.#]?[A-Za-z_][\w.#-]*)\s*\{",
        r"(?m)^\s*<([A-Za-z][\w:-]*)\b",
    )
    symbols: list[str] = []
    for pattern in patterns:
        symbols.extend(match.group(1) for match in re.finditer(pattern, text))
    return list(dict.fromkeys(symbols)), None


def _score(lines: list[str], symbols: list[str], valid: Optional[bool]) -> float:
    nonempty = sum(bool(line.strip()) for line in lines)
    todo = len(re.findall(r"(?i)\b(?:todo|fixme|placeholder|not implemented)\b", "\\n".join(lines)))
    duplicates = max(0, len(lines) - len(set(lines))) * 0.15
    return round(max(nonempty + len(symbols) * 8 + (25 if valid is True else 0) - todo * 3 - duplicates, 0), 2)


def analyze_file(path: str | Path) -> FileInfo:
    p = Path(path)
    text, encoding = read_text(p)
    lines = text.splitlines()
    extension = p.suffix.lower()
    if extension == ".py":
        symbols, valid = _python_symbols(text)
    elif extension in {".json", ".jsonc"}:
        symbols, valid = _generic_symbols(text)
        try:
            cleaned = re.sub(r"//.*?$|/\*.*?\*/", "", text, flags=re.M | re.S)
            json.loads(cleaned)
            valid = True
        except Exception:
            valid = False
    else:
        symbols, valid = _generic_symbols(text)
    return FileInfo(
        path=p, base_name=p.stem, extension=extension,
        canonical_base=canonical_base(p.name), encoding=encoding,
        syntax_valid=valid, lines=len(lines),
        nonempty_lines=sum(bool(x.strip()) for x in lines), symbols=symbols,
        score=_score(lines, symbols, valid),
    )


def analyze_files(paths: Iterable[str | Path]) -> list[FileInfo]:
    return [analyze_file(path) for path in paths]


def choose_base(infos: Iterable[FileInfo]) -> FileInfo:
    items = list(infos)
    if not items:
        raise ValueError("No files supplied")
    return max(items, key=lambda x: (x.score, x.syntax_valid is True, x.nonempty_lines, len(x.symbols)))


def _strip_json_comments(text: str) -> str:
    """Remove JSONC comments without touching strings, URLs or escaped quotes."""
    output: list[str] = []
    i = 0
    in_string = False
    escaped = False
    while i < len(text):
        char = text[i]
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            i += 1
            continue
        if char == '"':
            in_string = True
            output.append(char)
            i += 1
            continue
        if char == "/" and i + 1 < len(text) and text[i + 1] == "/":
            i += 2
            while i < len(text) and text[i] not in "\r\n":
                i += 1
            continue
        if char == "/" and i + 1 < len(text) and text[i + 1] == "*":
            i += 2
            while i + 1 < len(text) and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i = min(i + 2, len(text))
            continue
        output.append(char)
        i += 1
    return "".join(output)


def _parse_json_value(text: str, extension: str):
    cleaned = _strip_json_comments(text) if extension.lower() == ".jsonc" else text
    return json.loads(cleaned)


def validate_text(text: str, extension: str) -> tuple[bool, str]:
    ext = extension.lower()
    if ext == ".py":
        try:
            ast.parse(text)
            return True, ""
        except SyntaxError as exc:
            return False, f"Python inválido na linha {exc.lineno}: {exc.msg}"
    if ext in {".json", ".jsonc"}:
        try:
            _parse_json_value(text, ext)
            return True, ""
        except Exception as exc:
            return False, f"JSON inválido: {exc}"
    return True, ""


def backup_files(paths: Iterable[str | Path], root: str | Path | None = None) -> Path:
    items = [Path(p) for p in paths]
    if not items:
        raise ValueError("No files to backup")
    parent = Path(root) if root else items[0].parent / ".script_comparator_backup"
    backup = parent / datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup.mkdir(parents=True, exist_ok=False)
    for path in items:
        shutil.copy2(path, backup / path.name)
    return backup


def plan_version_names(base: str, extension: str, count: int) -> list[str]:
    return [f"{base}{index:03d}{extension}" for index in range(1, count + 1)]


def _python_blocks(text: str) -> dict[str, str]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return {}
    lines = text.splitlines(keepends=True)
    blocks: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            end = getattr(node, "end_lineno", node.lineno)
            blocks[node.name] = "".join(lines[node.lineno - 1:end])
    return blocks


def _insert_before_main_guard(text: str, blocks: list[str]) -> str:
    if not blocks:
        return text
    insertion = "\n\n".join(block.rstrip("\n") for block in blocks) + "\n\n"
    match = re.search(r"""(?m)^if __name__\s*==\s*["']__main__["']\s*:""", text)
    if match:
        return text[:match.start()].rstrip() + "\n\n" + insertion + text[match.start():]
    return text.rstrip() + "\n\n" + insertion


def _merge_python(base: str, others: list[tuple[str, str]]) -> tuple[str, list[str], list[Conflict], int]:
    result = base
    blocks = _python_blocks(base)
    additions: list[tuple[str, str]] = []
    conflicts: list[Conflict] = []
    for filename, text in others:
        for name, block in _python_blocks(text).items():
            if name not in blocks:
                if not any(existing == name for existing, _ in additions):
                    additions.append((name, block))
                continue
            if _norm(blocks[name]) == _norm(block):
                continue
            old_lines = [line for line in blocks[name].splitlines() if line.strip()]
            new_lines = [line for line in block.splitlines() if line.strip()]
            if len(new_lines) > len(old_lines) and all(line in new_lines for line in old_lines):
                result = result.replace(blocks[name], block, 1)
                blocks[name] = block
            else:
                conflicts.append(Conflict(
                    "python-symbol-conflict", name, "<base>", filename,
                    "Implementações diferentes; decisão manual necessária.",
                ))
    result = _insert_before_main_guard(result, [block for _, block in additions])
    return result, [name for name, _ in additions], conflicts, len(additions)


def _merge_json_values(target: dict, source: dict, filename: str, path: str = "") -> tuple[list[str], list[Conflict]]:
    added: list[str] = []
    conflicts: list[Conflict] = []
    for key, value in source.items():
        location = f"{path}.{key}" if path else key
        if key not in target:
            target[key] = value
            added.append(location)
        elif isinstance(target[key], dict) and isinstance(value, dict):
            nested_added, nested_conflicts = _merge_json_values(target[key], value, filename, location)
            added.extend(nested_added)
            conflicts.extend(nested_conflicts)
        elif target[key] != value:
            conflicts.append(Conflict(
                "json-key-conflict", location, "<base>", filename,
                "A mesma chave possui valores diferentes.",
            ))
    return added, conflicts


def _merge_json(base: str, others: list[tuple[str, str]], extension: str = ".json") -> tuple[str, list[str], list[Conflict], int]:
    try:
        result = _parse_json_value(base, extension)
    except Exception:
        return base, [], [Conflict("json-invalid", "<root>", "<base>", "<base>", "Base JSON inválido.")], 0
    if not isinstance(result, dict):
        return base, [], [Conflict("json-root", "<root>", "<base>", "<base>", "Raiz JSON não é objeto.")], 0
    added: list[str] = []
    conflicts: list[Conflict] = []
    for filename, text in others:
        try:
            obj = _parse_json_value(text, extension)
        except Exception:
            conflicts.append(Conflict("json-invalid", "<root>", "<base>", filename, "JSON de origem inválido."))
            continue
        if not isinstance(obj, dict):
            conflicts.append(Conflict("json-root", "<root>", "<base>", filename, "Raiz JSON de origem não é objeto."))
            continue
        new_added, new_conflicts = _merge_json_values(result, obj, filename)
        added.extend(new_added)
        conflicts.extend(new_conflicts)
    return json.dumps(result, ensure_ascii=False, indent=2) + "\n", added, conflicts, len(added)


def _line_anchors(lines: list[str]) -> list[tuple[int, str]]:
    anchors: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith(("//", "#", "/*", "*", "<!--")):
            anchors.append((index, stripped))
    return anchors


def _merge_generic(base: str, others: list[tuple[str, str]]) -> tuple[str, list[str], list[Conflict], int]:
    result = base
    chunks = 0
    for filename, text in others:
        base_lines = result.splitlines(keepends=True)
        other_lines = text.splitlines(keepends=True)
        matcher = difflib.SequenceMatcher(
            a=[_norm(line) for line in base_lines],
            b=[_norm(line) for line in other_lines],
            autojunk=False,
        )
        insertions: list[tuple[int, str]] = []
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag != "insert":
                continue
            chunk = "".join(other_lines[j1:j2])
            if not chunk.strip() or chunk in result:
                continue
            # Anchor the new block to the nearest unchanged line instead of appending blindly.
            anchor = max(0, min(i1, len(base_lines)))
            insertions.append((anchor, chunk))
        if insertions:
            for anchor, chunk in reversed(insertions):
                base_lines[anchor:anchor] = [chunk if chunk.endswith("\n") else chunk + "\n"]
            result = "".join(base_lines)
            chunks += len(insertions)
    return result, [], [], chunks


def _conflict_dict(conflict: Conflict) -> dict[str, str]:
    return asdict(conflict)


def preview_report(result: PreviewResult) -> dict:
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "report_type": "script_comparator.preview",
        "group": result.group,
        "base_file": result.base_file,
        "files": list(result.files),
        "final_file": result.final_file,
        "planned_original_names": list(result.planned_original_names),
        "strategy": result.strategy,
        "changed": result.changed,
        "validated": result.validated,
        "safe_to_consolidate": result.safe_to_consolidate,
        "added_symbols": list(result.added_symbols),
        "added_chunks": result.added_chunks,
        "conflicts": [_conflict_dict(c) for c in result.conflicts],
        "warnings": list(result.warnings),
    }


def merge_report(result: MergeResult) -> dict:
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "report_type": "script_comparator.merge",
        "group": result.group,
        "base_file": result.base_file,
        "output_file": result.output_file,
        "changed": result.changed,
        "validated": result.validated,
        "added_symbols": list(result.added_symbols),
        "added_chunks": result.added_chunks,
        "conflicts": [_conflict_dict(c) for c in result.conflicts],
        "backup_dir": result.backup_dir,
        "warnings": list(result.warnings),
    }


def report_json(result, *, indent: int = 2) -> str:
    if isinstance(result, PreviewResult):
        payload = preview_report(result)
    elif isinstance(result, MergeResult):
        payload = merge_report(result)
    else:
        raise TypeError("result must be PreviewResult or MergeResult")
    return json.dumps(payload, ensure_ascii=False, indent=indent, sort_keys=True) + "\n"


def write_report(result, path: str | Path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(report_json(result), encoding="utf-8", newline="")
    return target


def preview_group(
    paths: Iterable[str | Path],
    output_dir: str | Path | None = None,
    rename_originals: bool = True,
    validate: bool = True,
    allow_conflicts: bool = False,
) -> PreviewResult:
    """Build a complete consolidation plan without writing, renaming or backing up files."""
    files = [Path(path) for path in paths]
    if len(files) < 2:
        raise ValueError("São necessários pelo menos 2 ficheiros.")
    extensions = {path.suffix.lower() for path in files}
    if len(extensions) != 1:
        raise ValueError("Extensões diferentes devem ser grupos separados.")
    if any(not path.is_file() for path in files):
        raise FileNotFoundError("Um ou mais ficheiros não existem.")

    infos = analyze_files(files)
    base = choose_base(infos)
    base_text, _ = read_text(base.path)
    others = [(info.path.name, read_text(info.path)[0]) for info in infos if info.path != base.path]
    ext = base.extension
    if ext == ".py":
        merged, added, conflicts, chunks = _merge_python(base_text, others)
        strategy = "python-ast"
    elif ext in {".json", ".jsonc"}:
        merged, added, conflicts, chunks = _merge_json(base_text, others, ext)
        strategy = "json-structured"
    else:
        merged, added, conflicts, chunks = _merge_generic(base_text, others)
        strategy = "generic-contextual"

    if conflicts and not allow_conflicts:
        validated = False
        warnings = ["Consolidação bloqueada por conflitos; preview não escreve nada."]
    else:
        validated, reason = validate_text(merged, ext) if validate else (True, "")
        warnings = [reason] if not validated and reason else []

    destination = Path(output_dir) if output_dir else base.path.parent
    final = destination / f"{base.canonical_base}{ext}"
    planned = plan_version_names(base.canonical_base, ext, len(files)) if rename_originals else [p.name for p in files]
    safe = validated and (not conflicts or allow_conflicts)
    return PreviewResult(
        group=base.canonical_base,
        base_file=base.path.name,
        files=[p.name for p in files],
        final_file=str(final),
        planned_original_names=planned,
        strategy=strategy,
        changed=merged != base_text,
        validated=validated,
        added_symbols=added,
        added_chunks=chunks,
        conflicts=conflicts,
        warnings=warnings,
        safe_to_consolidate=safe,
    )


def consolidate_group(
    paths: Iterable[str | Path],
    output_dir: str | Path | None = None,
    backup_root: str | Path | None = None,
    rename_originals: bool = True,
    validate: bool = True,
    allow_conflicts: bool = False,
) -> MergeResult:
    files = [Path(path) for path in paths]
    if len(files) < 2:
        raise ValueError("São necessários pelo menos 2 ficheiros.")
    extensions = {path.suffix.lower() for path in files}
    if len(extensions) != 1:
        raise ValueError("Extensões diferentes devem ser grupos separados.")
    if any(not path.is_file() for path in files):
        raise FileNotFoundError("Um ou mais ficheiros não existem.")

    infos = analyze_files(files)
    base = choose_base(infos)
    base_text, encoding = read_text(base.path)
    others = [(info.path.name, read_text(info.path)[0]) for info in infos if info.path != base.path]
    ext = base.extension
    if ext == ".py":
        merged, added, conflicts, chunks = _merge_python(base_text, others)
    elif ext in {".json", ".jsonc"}:
        merged, added, conflicts, chunks = _merge_json(base_text, others, ext)
    else:
        merged, added, conflicts, chunks = _merge_generic(base_text, others)

    if conflicts and not allow_conflicts:
        return MergeResult(
            base.canonical_base, base.path.name, None, merged != base_text, False,
            added, chunks, conflicts, None,
            ["Consolidação bloqueada por conflitos; nenhuma alteração foi escrita."],
        )

    valid, reason = validate_text(merged, ext) if validate else (True, "")
    if not valid:
        return MergeResult(
            base.canonical_base, base.path.name, None, merged != base_text, False,
            added, chunks, conflicts, None, [reason],
        )

    destination = Path(output_dir) if output_dir else base.path.parent
    destination.mkdir(parents=True, exist_ok=True)
    final = destination / f"{base.canonical_base}{ext}"
    backup = backup_files(files, backup_root)

    if rename_originals:
        temp_dir = Path(tempfile.mkdtemp(prefix=".script_comparator_", dir=str(base.path.parent)))
        staged: list[Path] = []
        renamed: list[Path] = []
        try:
            for index, path in enumerate(files, 1):
                staged_path = temp_dir / f"{index:04d}{ext}"
                shutil.move(str(path), str(staged_path))
                staged.append(staged_path)
            planned = plan_version_names(base.canonical_base, ext, len(staged))
            for staged_path, name in zip(staged, planned):
                target = base.path.parent / name
                if target.exists():
                    raise FileExistsError(f"Nome de versão já existe: {target}")
                shutil.move(str(staged_path), str(target))
                renamed.append(target)
            final.write_text(merged, encoding=encoding, newline="")
        except Exception:
            # Best-effort rollback of only paths touched by this operation.
            for path in renamed:
                if path.exists():
                    path.unlink()
            for staged_path in staged:
                if staged_path.exists():
                    original_index = int(staged_path.stem) - 1
                    if 0 <= original_index < len(files):
                        shutil.move(str(staged_path), str(files[original_index]))
            raise
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    else:
        final.write_text(merged, encoding=encoding, newline="")

    return MergeResult(
        base.canonical_base, base.path.name, str(final), merged != base_text,
        True, added, chunks, conflicts, str(backup), [],
    )


def consolidate_all(paths: Iterable[str | Path], **kwargs) -> list[MergeResult]:
    return [
        consolidate_group(group, **kwargs)
        for group in group_files(paths).values()
        if len(group) >= 2
    ]


__all__ = [
    "FileInfo", "Conflict", "MergeResult", "PreviewResult", "read_text", "canonical_base",
    "group_files", "analyze_file", "analyze_files", "choose_base", "validate_text",
    "backup_files", "plan_version_names", "preview_group", "preview_report", "merge_report",
    "report_json", "write_report", "consolidate_group", "consolidate_all",
]
