"""Portable memory capsules for AI agents."""

from .merge import MergeReport, merge_capsules
from .schema import MemoryCapsule, MemoryItem
from .store import CapsuleStore
from .init import new_capsule

__all__ = [
    "MemoryCapsule",
    "MemoryItem",
    "CapsuleStore",
    "MergeReport",
    "merge_capsules",
    "new_capsule",
]
