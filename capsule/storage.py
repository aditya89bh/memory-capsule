"""Storage backends for memory capsules."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable

from .schema import MemoryCapsule
from .serializer import export_capsule, import_capsule


class StorageBackend(ABC):
    """Abstract persistence backend."""

    @abstractmethod
    def save_capsule(self, capsule: MemoryCapsule) -> None:
        raise NotImplementedError

    @abstractmethod
    def load_capsule(self, capsule_id: str) -> MemoryCapsule:
        raise NotImplementedError

    @abstractmethod
    def list_capsules(self) -> Iterable[str]:
        raise NotImplementedError


class JSONStorageBackend(StorageBackend):
    """Filesystem-backed JSON capsule storage."""

    def __init__(self, root: str | Path = "capsules"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, capsule_id: str) -> Path:
        return self.root / f"{capsule_id}.json"

    def save_capsule(self, capsule: MemoryCapsule) -> None:
        export_capsule(capsule, self._path(capsule.capsule_id))

    def load_capsule(self, capsule_id: str) -> MemoryCapsule:
        return import_capsule(self._path(capsule_id))

    def list_capsules(self) -> Iterable[str]:
        for path in self.root.glob("*.json"):
            yield path.stem
