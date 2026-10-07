from pathlib import Path

from script_comparator import (
    analyze_files,
    consolidate_group,
    group_files,
    preview_group,
    report_json,
    write_report,
)


def test_grouping_keeps_extensions_separate(tmp_path: Path):
    files = [tmp_path / "main.py", tmp_path / "main01.py", tmp_path / "main.js"]
    for p in files:
        p.write_text("x = 1\n", encoding="utf-8")
    groups = group_files(files)
    assert len(groups) == 2
    assert len(next(v for k, v in groups.items() if k[1] == ".py")) == 2


def test_python_missing_function_is_inserted_before_main(tmp_path: Path):
    base = tmp_path / "main.py"
    other = tmp_path / "main01.py"
    base.write_text('def existing():\n    return 1\n\ndef established():\n    return 3\n\nif __name__ == "__main__":\n    print(existing())\n', encoding="utf-8")
    other.write_text('def existing():\n    return 1\n\ndef recovered():\n    return 2\n', encoding="utf-8")
    result = consolidate_group([base, other])
    assert result.validated is True
    output = Path(result.output_file)
    text = output.read_text(encoding="utf-8")
    assert text.index("def recovered") < text.index('if __name__ == "__main__"')
    assert (tmp_path / "main001.py").exists()
    assert (tmp_path / "main002.py").exists()


def test_conflict_blocks_write_by_default(tmp_path: Path):
    a = tmp_path / "config.json"
    b = tmp_path / "config01.json"
    a.write_text('{"port": 8000}\n', encoding="utf-8")
    b.write_text('{"port": 9000}\n', encoding="utf-8")
    result = consolidate_group([a, b])
    assert result.validated is False
    assert result.output_file is None
    assert result.conflicts
    assert a.exists() and b.exists()


def test_preview_does_not_mutate_files_or_create_backup(tmp_path: Path):
    a = tmp_path / "main.py"
    b = tmp_path / "main01.py"
    a.write_text('def existing():\n    return 1\n\ndef established():\n    return 3\n\ndef helper():\n    return 4\n', encoding="utf-8")
    b.write_text('def existing():\n    return 1\n\ndef recovered():\n    return 2\n', encoding="utf-8")
    before = {p.name: p.read_bytes() for p in (a, b)}
    result = preview_group([a, b])
    assert result.safe_to_consolidate is True
    assert result.final_file.endswith("main.py")
    assert result.planned_original_names == ["main001.py", "main002.py"]
    assert "recovered" in result.added_symbols
    assert {p.name: p.read_bytes() for p in (a, b)} == before
    assert not (tmp_path / ".script_comparator_backup").exists()


def test_js_ts_missing_function_is_recovered(tmp_path: Path):
    base = tmp_path / "app.ts"
    other = tmp_path / "app01.ts"
    base.write_text(
        "export function existing(): number {\n    return 1;\n}\n\n"
        "export function established(): number {\n    return 3;\n}\n",
        encoding="utf-8",
    )
    other.write_text(
        "export function existing(): number {\n    return 1;\n}\n\n"
        "export function recovered(): number {\n    return 2;\n}\n",
        encoding="utf-8",
    )
    result = consolidate_group([base, other])
    assert result.validated is True
    text = Path(result.output_file).read_text(encoding="utf-8")
    assert "function recovered" in text
    assert result.added_symbols == ["recovered"]


def test_js_ts_conflict_blocks_write(tmp_path: Path):
    a = tmp_path / "app.js"
    b = tmp_path / "app01.js"
    a.write_text("function run() {\n  return 1;\n}\n", encoding="utf-8")
    b.write_text("function run() {\n  return 2;\n}\n", encoding="utf-8")
    result = consolidate_group([a, b])
    assert result.validated is False
    assert result.output_file is None
    assert any(c.kind == "js-ts-symbol-conflict" for c in result.conflicts)
    assert a.exists() and b.exists()


def test_json_nested_keys_are_recovered(tmp_path: Path):
    a = tmp_path / "config.json"
    b = tmp_path / "config01.json"
    a.write_text('{"database": {"host": "localhost"}}\n', encoding="utf-8")
    b.write_text('{"database": {"port": 5432, "ssl": true}}\n', encoding="utf-8")
    result = consolidate_group([a, b])
    assert result.validated is True
    text = Path(result.output_file).read_text(encoding="utf-8")
    assert '"port": 5432' in text
    assert '"ssl": true' in text


def test_jsonc_comments_and_urls_are_parsed_safely(tmp_path: Path):
    a = tmp_path / "config.jsonc"
    b = tmp_path / "config01.jsonc"
    a.write_text(
        '// base comment\n{"api": {"url": "https://example.com/a"}}\n',
        encoding="utf-8",
    )
    b.write_text(
        '/* extra */\n{"api": {"timeout": 30}}\n',
        encoding="utf-8",
    )
    result = consolidate_group([a, b])
    assert result.validated is True
    text = Path(result.output_file).read_text(encoding="utf-8")
    assert '"url": "https://example.com/a"' in text
    assert '"timeout": 30' in text


def test_preview_detects_conflict_without_mutation(tmp_path: Path):
    a = tmp_path / "config.json"
    b = tmp_path / "config01.json"
    a.write_text('{"port": 8000}\n', encoding="utf-8")
    b.write_text('{"port": 9000}\n', encoding="utf-8")
    result = preview_group([a, b])
    assert result.safe_to_consolidate is False
    assert result.validated is False
    assert result.conflicts
    assert a.exists() and b.exists()
