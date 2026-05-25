"""Merge utilities for portable memory capsules."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from .schema import MemoryCapsule, MemoryItem


@dataclass
class MergeReport:
    """Summary of a capsule merge operation."""

    added: int = 0
    skipped_duplicates: int = 0
    conflicts: List[str] = field(default_factory=list)

    @property
    def total_conflicts(self) -> int:
        return len(self.conflicts)


def _memory_key(memory: MemoryItem) -> Tuple[str, str, Tuple[str, ...]]:
    """Stable duplicate key based on content, type, and tags."""
    return (
        memory.text.strip().lower(),
        memory.kind.strip().lower(),
        tuple(sorted(tag.strip().lower() for tag in memory.tags)),
    )


def merge_capsules(
    base: MemoryCapsule,
    incoming: MemoryCapsule,
    *,
    source_label: str | None = None,
) -> tuple[MemoryCapsule, MergeReport]:
    """Merge incoming memories into base without duplicating identical entries.

    The merge strategy is intentionally conservative:
    - exact semantic duplicates by text, kind, and tags are skipped
    - different memories are appended
    - metadata records the merge source for traceability
    - owner mismatches are reported as conflicts but do not block merging
    """
    report = MergeReport()
    merged = base.model_copy(deep=True)
    existing_keys: Dict[Tuple[str, str, Tuple[str, ...]], str] = {
        _memory_key(memory): memory.id for memory in merged.memories
    }

    if base.owner != incoming.owner:
        report.conflicts.append(
            f"owner mismatch: base={base.owner!r}, incoming={incoming.owner!r}"
        )

    label = source_label or incoming.agent or incoming.capsule_id

    for memory in incoming.memories:
        key = _memory_key(memory)
        if key in existing_keys:
            report.skipped_duplicates += 1
            continue

        item = memory.model_copy(deep=True)
        item.metadata = dict(item.metadata)
        item.metadata.setdefault("merged_from", label)
        merged.memories.append(item)
        existing_keys[key] = item.id
        report.added += 1

    merged.metadata = dict(merged.metadata)
    merged.metadata.setdefault("merged_sources", [])
    if label not in merged.metadata["merged_sources"]:
        merged.metadata["merged_sources"].append(label)
    merged.touch()
    return merged, report
