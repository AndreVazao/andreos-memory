from pathlib import Path

from script_comparator import preview_group, report_json, write_report


def test_preview_report_is_stable_and_writeable(tmp_path: Path):
    a = tmp_path / "main.py"
    b = tmp_path / "main01.py"
    a.write_text("def existing():\n    return 1\n", encoding="utf-8")
    b.write_text("def recovered():\n    return 2\n", encoding="utf-8")

    result = preview_group([a, b])
    payload = __import__("script_comparator").preview_report(result)

    assert payload["schema_version"] == "1.0"
    assert payload["report_type"] == "script_comparator.preview"
    assert payload["safe_to_consolidate"] is True
    assert "recovered" in payload["added_symbols"]
    assert report_json(result) == report_json(result)

    target = write_report(result, tmp_path / "reports" / "preview.json")
    assert target.exists()
    assert target.read_text(encoding="utf-8") == report_json(result)


def test_merge_report_contains_stable_contract(tmp_path: Path):
    a = tmp_path / "main.py"
    b = tmp_path / "main01.py"
    a.write_text("def existing():\n    return 1\n", encoding="utf-8")
    b.write_text("def recovered():\n    return 2\n", encoding="utf-8")

    from script_comparator import consolidate_group, merge_report

    result = consolidate_group([a, b])
    payload = merge_report(result)

    assert payload["schema_version"] == "1.0"
    assert payload["report_type"] == "script_comparator.merge"
    assert payload["validated"] is True
    assert payload["output_file"].endswith("main.py")
