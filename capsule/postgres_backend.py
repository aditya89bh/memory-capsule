"""PostgreSQL backend scaffold.

This module defines the production-oriented backend interface for larger
multi-agent deployments. Full async pooling and migrations can be layered on
later.
"""
from __future__ import annotations

from typing import Iterable

from .schema import MemoryCapsule
from .storage import StorageBackend


class PostgresStorageBackend(StorageBackend):
    """Production PostgreSQL persistence backend scaffold."""

    def __init__(self, connection_url: str):
        self.connection_url = connection_url

    def save_capsule(self, capsule: MemoryCapsule) -> None:
        raise NotImplementedError(
            "PostgreSQL persistence implementation is planned for a future release"
        )

    def load_capsule(self, capsule_id: str) -> MemoryCapsule:
        raise NotImplementedError(
            "PostgreSQL persistence implementation is planned for a future release"
        )

    def list_capsules(self) -> Iterable[str]:
        raise NotImplementedError(
            "PostgreSQL persistence implementation is planned for a future release"
        )
