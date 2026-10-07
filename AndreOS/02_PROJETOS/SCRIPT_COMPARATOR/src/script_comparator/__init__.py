"""Reusable Script Comparator & Consolidator public API."""

from .core import (
    Conflict,
    FileInfo,
    MergeResult,
    PreviewResult,
    analyze_file,
    analyze_files,
    backup_files,
    canonical_base,
    choose_base,
    consolidate_all,
    consolidate_group,
    group_files,
    plan_version_names,
    preview_group,
    preview_report,
    merge_report,
    report_json,
    write_report,
    read_text,
    validate_text,
)

__all__ = [
    "Conflict", "FileInfo", "MergeResult", "PreviewResult", "read_text", "canonical_base",
    "group_files", "analyze_file", "analyze_files", "choose_base",
    "validate_text", "backup_files", "plan_version_names", "preview_group",
    "preview_report", "merge_report", "report_json", "write_report",
    "consolidate_group", "consolidate_all",
]
