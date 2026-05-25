"""SQLite persistence backend for memory capsules."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable

from .schema import MemoryCapsule
from .storage import StorageBackend


class SQLiteStorageBackend(StorageBackend):
    """SQLite-backed capsule persistence."""

    def __init__(self, database_path: str | Path = "memory_capsule.db"):
        self.database_path = str(database_path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS capsules (
                    capsule_id TEXT PRIMARY KEY,
                    owner TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            connection.commit()

    def save_capsule(self, capsule: MemoryCapsule) -> None:
        payload = capsule.model_dump_json()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO capsules (capsule_id, owner, payload, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(capsule_id)
                DO UPDATE SET
                    owner=excluded.owner,
                    payload=excluded.payload,
                    updated_at=excluded.updated_at
                """,
                (
                    capsule.capsule_id,
                    capsule.owner,
                    payload,
                    capsule.updated_at.isoformat(),
                ),
            )
            connection.commit()

    def load_capsule(self, capsule_id: str) -> MemoryCapsule:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT payload FROM capsules WHERE capsule_id = ?",
                (capsule_id,),
            ).fetchone()

        if row is None:
            raise KeyError(f"Capsule not found: {capsule_id}")

        return MemoryCapsule.model_validate_json(row[0])

    def list_capsules(self) -> Iterable[str]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT capsule_id FROM capsules ORDER BY updated_at DESC"
            ).fetchall()

        for row in rows:
            yield row[0]
