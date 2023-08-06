from __future__ import annotations
import sys
from pathlib import Path


def get_venv() -> Path|None:
    """
    Return the path to the virtual environment if Python runs inside a virtual environment, None otherwise.
    """
    base_prefix = getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix
    if base_prefix == sys.prefix:
        return None
    return Path(sys.prefix)


def is_in_venv(path: Path|str) -> bool:
    if not isinstance(path, Path):
        path = Path(path)
    venv = get_venv()
    if venv is None:
        return False
    return venv in path.parents
