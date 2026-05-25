"""Semantic retrieval for memory capsules.

This module is optional. It uses SentenceTransformers for embeddings and FAISS
for nearest-neighbor search when the optional dependencies are installed.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np

from .embeddings import embed_texts
from .retrieval import keyword_search
from .schema import MemoryCapsule, MemoryItem


@dataclass
class SemanticSearchResult:
    """A memory item returned by semantic search."""

    memory: MemoryItem
    score: float


def _memory_text(memory: MemoryItem) -> str:
    tags = " ".join(memory.tags)
    return " ".join(part for part in [memory.kind, tags, memory.text] if part)


def semantic_search(
    capsule: MemoryCapsule,
    query: str,
    *,
    limit: int = 5,
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    fallback_to_keyword: bool = True,
) -> List[SemanticSearchResult]:
    """Search capsule memories using embeddings and FAISS.

    If optional semantic dependencies are unavailable and fallback_to_keyword is
    true, the function returns keyword-ranked results with score 0.0.
    """
    if not capsule.memories:
        return []

    try:
        import faiss  # type: ignore
    except Exception as exc:  # pragma: no cover - environment dependent
        if not fallback_to_keyword:
            raise RuntimeError("FAISS is required for semantic search") from exc
        return [SemanticSearchResult(memory=item, score=0.0) for item in keyword_search(capsule, query, limit=limit)]

    try:
        texts = [_memory_text(memory) for memory in capsule.memories]
        memory_vectors = embed_texts(texts, model_name=model_name).astype("float32")
        query_vector = embed_texts([query], model_name=model_name).astype("float32")
    except Exception as exc:  # pragma: no cover - model download/environment dependent
        if not fallback_to_keyword:
            raise RuntimeError("Embedding model failed during semantic search") from exc
        return [SemanticSearchResult(memory=item, score=0.0) for item in keyword_search(capsule, query, limit=limit)]

    dimension = memory_vectors.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(np.ascontiguousarray(memory_vectors))
    scores, indices = index.search(np.ascontiguousarray(query_vector), min(limit, len(capsule.memories)))

    results: List[SemanticSearchResult] = []
    for score, index_position in zip(scores[0], indices[0]):
        if index_position < 0:
            continue
        results.append(SemanticSearchResult(memory=capsule.memories[int(index_position)], score=float(score)))
    return results
