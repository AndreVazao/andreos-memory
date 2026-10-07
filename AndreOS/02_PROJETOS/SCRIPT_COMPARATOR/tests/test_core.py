from pathlib import Path

from script_comparator import analyze_files, consolidate_group, group_files


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
    base.write_text('def existing():\n    return 1\n\nif __name__ == "__main__":\n    print(existing())\n', encoding="utf-8")
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
