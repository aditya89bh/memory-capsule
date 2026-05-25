"""Keyword retrieval for memory capsules."""
from __future__ import annotations

import re
from typing import List, Tuple

from .schema import MemoryCapsule, MemoryItem


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def keyword_search(capsule: MemoryCapsule, query: str, limit: int = 5) -> List[MemoryItem]:
    """Return memories ranked by simple token overlap with text, tags, and kind."""
    q = _tokens(query)
    scored: List[Tuple[int, MemoryItem]] = []
    for item in capsule.memories:
        haystack = " ".join([item.text, item.kind, " ".join(item.tags)])
        score = len(q & _tokens(haystack))
        if score:
            scored.append((score, item))
    scored.sort(key=lambda pair: (pair[0], pair[1].created_at), reverse=True)
    return [item for _, item in scored[:limit]]
