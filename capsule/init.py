"""Factory helpers for creating new memory capsules."""
from __future__ import annotations

from .schema import MemoryCapsule
from .store import CapsuleStore


def new_capsule(owner: str, agent: str | None = None, summary: str = "") -> CapsuleStore:
    return CapsuleStore(MemoryCapsule(owner=owner, agent=agent, summary=summary))
