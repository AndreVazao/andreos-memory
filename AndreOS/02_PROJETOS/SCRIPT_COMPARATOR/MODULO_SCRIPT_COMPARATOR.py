"""AndreOS Script Comparator & Consolidator.
Reusable core module; no GUI dependencies.
"""
from __future__ import annotations
import ast, difflib, hashlib, json, re, shutil, tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional

FINAL_MARKERS=("_final","-final","_latest","-latest","_complete","-complete")
VERSION_RE=re.compile(r"(?i)(?:[_\\-. ]?(?:v)?\\d+)$")
TEXT_EXTENSIONS={".py",".js",".jsx",".ts",".tsx",".json",".jsonc",".css",".scss",".html",".htm",".kt",".kts",".java",".cs",".c",".h",".cpp",".hpp",".xml",".yaml",".yml",".md",".txt",".sql",".sh",".bat",".ps1",".toml",".ini",".cfg",".vue",".svelte"}

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
    symbols: list[str]=field(default_factory=list)
    score: float=0.0

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
    added_symbols: list[str]=field(default_factory=list)
    added_chunks: int=0
    conflicts: list[Conflict]=field(default_factory=list)
    backup_dir: Optional[str]=None
    warnings: list[str]=field(default_factory=list)

def read_text(path):
    data=Path(path).read_bytes()
    for enc in ("utf-8","utf-8-sig","cp1252","latin-1"):
        try: return data.decode(enc),enc
        except UnicodeDecodeError: pass
    raise ValueError(f"Unsupported text encoding: {path}")

def canonical_base(name):
    stem=Path(name).stem
    low=stem.lower()
    for marker in FINAL_MARKERS:
        if low.endswith(marker):
            stem=stem[:-len(marker)]; break
    stem=VERSION_RE.sub("",stem)
    stem=re.sub(r"[_\\-. ]+$","",stem)
    return stem or Path(name).stem

def group_key(path):
    p=Path(path); return canonical_base(p.name).casefold(),p.suffix.lower()

def group_files(paths: Iterable[str|Path]):
    out={}
    for raw in paths:
        p=Path(raw); out.setdefault(group_key(p),[]).append(p)
    return out

def _norm(s): return re.sub(r"\\s+"," ",s.strip())

def _python_symbols(text):
    try: tree=ast.parse(text)
    except SyntaxError: return [],False
    symbols=[]
    for n in tree.body:
        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)): symbols.append(n.name)
        elif isinstance(n,(ast.Import,ast.ImportFrom)):
            symbols.append("import")
    return list(dict.fromkeys(symbols)),True

def _generic_symbols(text):
    pats=[
        r"(?m)^\\s*(?:export\\s+)?(?:async\\s+)?function\\s+([A-Za-z_$][\\w$]*)",
        r"(?m)^\\s*(?:export\\s+)?class\\s+([A-Za-z_$][\\w$]*)",
        r"(?m)^\\s*(?:fun|def)\\s+([A-Za-z_]\\w*)",
        r"(?m)^\\s*([.#]?[A-Za-z_][\\w.#-]*)\\s*\\{",
        r"(?m)^\\s*<([A-Za-z][\\w:-]*)\\b",
    ]
    out=[]
    for pat in pats: out += [m.group(1) for m in re.finditer(pat,text)]
    return list(dict.fromkeys(out)),None

def _score(lines,symbols,valid):
    nonempty=sum(bool(x.strip()) for x in lines)
    todo=len(re.findall(r"(?i)\\b(?:todo|fixme|placeholder|not implemented)\\b","\\n".join(lines)))
    dup=max(0,len(lines)-len(set(lines)))*.15
    return round(max(nonempty+len(symbols)*8+(25 if valid is True else 0)-todo*3-dup,0),2)

def analyze_file(path):
    p=Path(path); text,enc=read_text(p); ext=p.suffix.lower(); lines=text.splitlines()
    if ext==".py": symbols,valid=_python_symbols(text)
    elif ext in {".json",".jsonc"}:
        symbols,valid=_generic_symbols(text)
        try: json.loads(re.sub(r"//.*?$|/\\*.*?\\*/","",text,flags=re.M|re.S)); valid=True
        except Exception: valid=False
    else: symbols,valid=_generic_symbols(text)
    return FileInfo(p,p.stem,ext,canonical_base(p.name),enc,valid,len(lines),sum(bool(x.strip()) for x in lines),symbols,_score(lines,symbols,valid))

def analyze_files(paths): return [analyze_file(p) for p in paths]

def choose_base(infos):
    if not infos: raise ValueError("No files supplied")
    return max(infos,key=lambda x:(x.score,x.syntax_valid is True,x.nonempty_lines,len(x.symbols)))

def validate_text(text,ext):
    if ext==".py":
        try: ast.parse(text); return True,""
        except SyntaxError as e: return False,f"Python inválido na linha {e.lineno}: {e.msg}"
    if ext in {".json",".jsonc"}:
        try: json.loads(re.sub(r"//.*?$|/\\*.*?\\*/","",text,flags=re.M|re.S)); return True,""
        except Exception as e: return False,f"JSON inválido: {e}"
    return True,""

def backup_files(paths,root=None):
    paths=list(paths)
    if not paths: raise ValueError("No files to backup")
    parent=Path(root) if root else paths[0].parent/".script_comparator_backup"
    backup=parent/datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup.mkdir(parents=True,exist_ok=False)
    for p in paths: shutil.copy2(p,backup/p.name)
    return backup

def plan_version_names(base,ext,count):
    return [f"{base}{i:03d}{ext}" for i in range(1,count+1)]

def _py_blocks(text):
    try: tree=ast.parse(text)
    except SyntaxError: return {}
    lines=text.splitlines(keepends=True); out={}
    for n in tree.body:
        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
            end=getattr(n,"end_lineno",n.lineno); out[n.name]="".join(lines[n.lineno-1:end])
    return out

def _merge_python(base,others):
    result=base; blocks=_py_blocks(base); added=[]; conflicts=[]
    for filename,text in others:
        for name,block in _py_blocks(text).items():
            if name not in blocks:
                added.append((name,block.rstrip()+"\\n")); continue
            if _norm(blocks[name])!=_norm(block):
                old=[x for x in blocks[name].splitlines() if x.strip()]
                new=[x for x in block.splitlines() if x.strip()]
                if len(new)>len(old) and all(x in new for x in old):
                    result=result.replace(blocks[name],block,1); blocks[name]=block
                else:
                    conflicts.append(Conflict("python-symbol-conflict",name,"<base>",filename,"Implementações diferentes; decisão manual necessária."))
    if added:
        # Insert before a module-level main guard when present, otherwise before final content.
        marker='if __name__ == "__main__":'
        text="\n".join(b for _,b in added)
        pos=result.find(marker)
        if pos>=0: result=result[:pos].rstrip()+"\n\n"+text+"\n"+result[pos:]
        else: result=result.rstrip()+"\n\n"+text
    return result,[n for n,_ in added],conflicts,len(added)

def _merge_json(base,others):
    try: result=json.loads(base)
    except Exception: return base,[],[Conflict("json-invalid","<root>","<base>","<base>","Base JSON inválido.")],0
    if not isinstance(result,dict): return base,[],[Conflict("json-root","<root>","<base>","<base>","Raiz JSON não é objeto.")],0
    added=[]; conflicts=[]
    for filename,text in others:
        try: obj=json.loads(text)
        except Exception:
            conflicts.append(Conflict("json-invalid","<root>","<base>",filename,"JSON de origem inválido.")); continue
        if not isinstance(obj,dict):
            conflicts.append(Conflict("json-root","<root>","<base>",filename,"Raiz JSON de origem não é objeto.")); continue
        for k,v in obj.items():
            if k not in result: result[k]=v; added.append(k)
            elif result[k]!=v: conflicts.append(Conflict("json-key-conflict",k,"<base>",filename,"A mesma chave possui valores diferentes."))
    return json.dumps(result,ensure_ascii=False,indent=2)+"\n",added,conflicts,len(added)

def _merge_generic(base,others):
    result=base; chunks=0
    for filename,text in others:
        a=result.splitlines(keepends=True); b=text.splitlines(keepends=True)
        sm=difflib.SequenceMatcher(a=[_norm(x) for x in a],b=[_norm(x) for x in b],autojunk=False)
        additions=[]
        for tag,i1,i2,j1,j2 in sm.get_opcodes():
            if tag=="insert":
                chunk="".join(b[j1:j2])
                if chunk.strip() and chunk not in result: additions.append(chunk)
        if additions:
            result=result.rstrip()+"\n\n"+"\n".join(x.rstrip("\n") for x in additions)+"\n"; chunks+=len(additions)
    return result,[],[],chunks

def consolidate_group(paths,output_dir=None,backup_root=None,rename_originals=True,validate=True):
    files=[Path(p) for p in paths]
    if len(files)<2: raise ValueError("São necessários pelo menos 2 ficheiros.")
    exts={p.suffix.lower() for p in files}
    if len(exts)!=1: raise ValueError("Extensões diferentes devem ser grupos separados.")
    infos=analyze_files(files); base=choose_base(infos); ext=base.extension
    base_text,enc=read_text(base.path)
    others=[(x.path.name,read_text(x.path)[0]) for x in infos if x.path!=base.path]
    if ext==".py": merged,added,conflicts,chunks=_merge_python(base_text,others)
    elif ext in {".json",".jsonc"}: merged,added,conflicts,chunks=_merge_json(base_text,others)
    else: merged,added,conflicts,chunks=_merge_generic(base_text,others)
    valid,reason=validate_text(merged,ext) if validate else (True,"")
    if not valid: return MergeResult(base.canonical_base,base.path.name,None,merged!=base_text,False,added,chunks,conflicts,None,[reason])
    backup=None
    dest=Path(output_dir) if output_dir else base.path.parent
    dest.mkdir(parents=True,exist_ok=True)
    final=dest/f"{base.canonical_base}{ext}"
    if rename_originals:
        backup=backup_files(files,backup_root)
        tmp=Path(tempfile.mkdtemp(prefix=".script_comparator_",dir=str(base.path.parent)))
        try:
            staged=[]
            for i,p in enumerate(files,1):
                q=tmp/f"{i:04d}{ext}"; shutil.move(str(p),str(q)); staged.append(q)
            for i,q in enumerate(staged,1): shutil.move(str(q),str(base.path.parent/f"{base.canonical_base}{i:03d}{ext}"))
            final.write_text(merged,encoding=enc,newline="")
        finally: shutil.rmtree(tmp,ignore_errors=True)
    else: final.write_text(merged,encoding=enc,newline="")
    return MergeResult(base.canonical_base,base.path.name,str(final),merged!=base_text,True,added,chunks,conflicts,str(backup) if backup else None,[])

def consolidate_all(paths,**kwargs):
    return [consolidate_group(group,**kwargs) for group in group_files(paths).values() if len(group)>=2]

__all__=["FileInfo","Conflict","MergeResult","read_text","canonical_base","group_files","analyze_file","analyze_files","choose_base","validate_text","backup_files","plan_version_names","consolidate_group","consolidate_all"]
