"""Simple in-process metrics collection."""
from __future__ import annotations

from collections import Counter

_metrics = Counter()


def increment(metric: str) -> None:
    _metrics[metric] += 1


def snapshot() -> dict[str, int]:
    return dict(_metrics)
