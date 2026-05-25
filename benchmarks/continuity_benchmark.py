"""Simple retrieval benchmark for memory-capsule."""
from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

from capsule import new_capsule
from capsule.retrieval import keyword_search
from capsule.semantic import semantic_search


@dataclass
class BenchmarkCase:
    query: str
    expected_term: str


CASES = [
    BenchmarkCase(
        query="How should robots preserve continuity between shifts?",
        expected_term="continuity",
    ),
    BenchmarkCase(
        query="What systems do operators prefer?",
        expected_term="inspectable",
    ),
    BenchmarkCase(
        query="How should memory remain portable?",
        expected_term="portable",
    ),
]


def build_capsule():
    store = new_capsule(owner="benchmark-lab", agent="benchmark-agent")

    store.add_memory(
        "Portable memory capsules preserve continuity between agents and sessions.",
        kind="thesis",
        tags=["continuity", "memory"],
    )
    store.add_memory(
        "Operators prefer inspectable automation systems.",
        kind="ux",
        tags=["trust", "operators"],
    )
    store.add_memory(
        "Robotic systems should adapt gradually across production shifts.",
        kind="robotics",
        tags=["adaptation", "robots"],
    )
    return store.capsule


def keyword_score(capsule, case: BenchmarkCase) -> float:
    results = keyword_search(capsule, case.query, limit=1)
    if not results:
        return 0.0
    return float(case.expected_term.lower() in results[0].text.lower())


def semantic_score(capsule, case: BenchmarkCase) -> float:
    results = semantic_search(capsule, case.query, limit=1)
    if not results:
        return 0.0
    return float(case.expected_term.lower() in results[0].memory.text.lower())


def main() -> None:
    capsule = build_capsule()

    keyword_scores = [keyword_score(capsule, case) for case in CASES]
    semantic_scores = [semantic_score(capsule, case) for case in CASES]

    print("Retrieval Benchmark")
    print("-------------------")
    print(f"cases: {len(CASES)}")
    print(f"keyword score: {mean(keyword_scores):.2f}")
    print(f"semantic score: {mean(semantic_scores):.2f}")


if __name__ == "__main__":
    main()
