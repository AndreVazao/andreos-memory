"""Compatibility entry point for older integrations.

New projects should depend on the package in src/script_comparator.
This file intentionally re-exports the same public API so existing imports
continue to work while hosts migrate to the package layout.
"""
from pathlib import Path
import sys

_PACKAGE_ROOT = Path(__file__).resolve().parent / "src"
if str(_PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(_PACKAGE_ROOT))

from script_comparator import *  # noqa: F401,F403,E402
