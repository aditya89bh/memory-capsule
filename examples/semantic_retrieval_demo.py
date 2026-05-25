"""Demonstrate semantic retrieval over memory capsules."""
from __future__ import annotations

from capsule import new_capsule
from capsule.semantic import semantic_search


def build_demo_capsule():
    store = new_capsule(
        owner="research-lab",
        agent="research-agent",
        summary="Semantic retrieval example for memory-capsule.",
    )
    store.add_memory(
        "Factory robots should adapt to operational drift over time.",
        kind="principle",
        tags=["robotics", "adaptation"],
    )
    store.add_memory(
        "Portable memory helps agents preserve continuity between sessions.",
        kind="thesis",
        tags=["memory", "continuity"],
    )
    store.add_memory(
        "Operators prefer transparent and inspectable automation systems.",
        kind="preference",
        tags=["ux", "trust"],
    )
    return store.capsule


def main() -> None:
    capsule = build_demo_capsule()

    print("Semantic retrieval results")
    print("--------------------------")

    results = semantic_search(capsule, "How should agents preserve continuity?", limit=3)

    for result in results:
        print(f"score={result.score:.4f} [{result.memory.kind}] {result.memory.text}")


if __name__ == "__main__":
    main()
