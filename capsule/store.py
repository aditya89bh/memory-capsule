"""Simple JSON-backed memory capsule store."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

from .schema import MemoryCapsule, MemoryItem
from .serializer import import_capsule, export_capsule


class CapsuleStore:
    """In-memory capsule with save/load helpers."""

    def __init__(self, capsule: Optional[MemoryCapsule] = None):
        self.capsule = capsule or MemoryCapsule()

    def add_memory(self, text: str, kind: str = "note", tags: Optional[Iterable[str]] = None, **metadata) -> MemoryItem:
        item = MemoryItem(text=text, kind=kind, tags=list(tags or []), metadata=metadata)
        self.capsule.memories.append(item)
        self.capsule.touch()
        return item

    def save(self, path: str | Path) -> Path:
        return export_capsule(self.capsule, path)

    @classmethod
    def load(cls, path: str | Path) -> "CapsuleStore":
        return cls(import_capsule(path))
