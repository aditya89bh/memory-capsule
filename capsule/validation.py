"""Validation helpers for memory capsules."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .schema import MemoryCapsule


@dataclass
class ValidationReport:
    """Result of validating a memory capsule."""

    valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        self.valid = False
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)


def validate_capsule(capsule: MemoryCapsule) -> ValidationReport:
    """Validate a capsule for production use."""
    report = ValidationReport()

    if not capsule.capsule_id.strip():
        report.add_error("capsule_id is required")

    if not capsule.owner.strip():
        report.add_error("owner is required")

    seen_memory_ids: set[str] = set()
    for index, memory in enumerate(capsule.memories):
        prefix = f"memories[{index}]"

        if not memory.id.strip():
            report.add_error(f"{prefix}.id is required")

        if memory.id in seen_memory_ids:
            report.add_error(f"duplicate memory id: {memory.id}")
        seen_memory_ids.add(memory.id)

        if not memory.text.strip():
            report.add_error(f"{prefix}.text is required")

        if not memory.kind.strip():
            report.add_error(f"{prefix}.kind is required")

        if len(memory.text) > 10_000:
            report.add_warning(f"{prefix}.text is unusually long")

    return report
