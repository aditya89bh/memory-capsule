"""Portable memory capsules for AI agents."""

from .merge import MergeReport, merge_capsules
from .schema import MemoryCapsule, MemoryItem
from .semantic import SemanticSearchResult, semantic_search
from .store import CapsuleStore
from .init import new_capsule

__all__ = [
    "MemoryCapsule",
    "MemoryItem",
    "CapsuleStore",
    "MergeReport",
    "SemanticSearchResult",
    "merge_capsules",
    "semantic_search",
    "new_capsule",
]
