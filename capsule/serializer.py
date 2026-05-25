"""Import/export helpers for capsule JSON files."""
from __future__ import annotations

from pathlib import Path

from .schema import MemoryCapsule


def export_capsule(capsule: MemoryCapsule, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(capsule.model_dump_json(indent=2), encoding="utf-8")
    return path


def import_capsule(path: str | Path) -> MemoryCapsule:
    return MemoryCapsule.model_validate_json(Path(path).read_text(encoding="utf-8"))
