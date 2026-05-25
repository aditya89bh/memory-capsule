"""Schema migration utilities for memory capsules."""
from __future__ import annotations

from typing import Any, Callable, Dict

CURRENT_SCHEMA_VERSION = "0.2.0"

MigrationFunction = Callable[[dict[str, Any]], dict[str, Any]]


class MigrationError(RuntimeError):
    """Raised when a schema migration fails."""


MIGRATIONS: Dict[tuple[str, str], MigrationFunction] = {}


def migration(source: str, target: str):
    """Register a migration function."""

    def decorator(function: MigrationFunction) -> MigrationFunction:
        MIGRATIONS[(source, target)] = function
        return function

    return decorator


@migration("0.1.0", "0.2.0")
def migrate_010_to_020(payload: dict[str, Any]) -> dict[str, Any]:
    """Upgrade older capsules to the 0.2.0 schema."""
    payload = dict(payload)
    payload.setdefault("metadata", {})
    payload["version"] = "0.2.0"
    return payload


def migrate_payload(payload: dict[str, Any], target_version: str = CURRENT_SCHEMA_VERSION) -> dict[str, Any]:
    """Apply sequential migrations until the target version is reached."""
    current_version = payload.get("version", "0.1.0")

    if current_version == target_version:
        return payload

    migration_key = (current_version, target_version)

    if migration_key not in MIGRATIONS:
        raise MigrationError(
            f"No migration path from {current_version} to {target_version}"
        )

    migrated = MIGRATIONS[migration_key](payload)
    migrated["version"] = target_version
    return migrated
