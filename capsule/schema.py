"""Pydantic schemas for portable agent memory capsules."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class MemoryItem(BaseModel):
    """A single durable memory entry."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    text: str
    kind: str = "note"
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MemoryCapsule(BaseModel):
    """Portable memory state that can move between agents or runtimes."""

    capsule_id: str = Field(default_factory=lambda: str(uuid4()))
    owner: str = "unknown"
    agent: Optional[str] = None
    version: str = "0.1.0"
    summary: str = ""
    memories: List[MemoryItem] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc)
