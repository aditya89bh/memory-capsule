from capsule import new_capsule
from capsule.semantic import semantic_search


def test_semantic_search_returns_results():
    store = new_capsule(owner="research")

    store.add_memory(
        "Portable memory preserves continuity across sessions.",
        kind="thesis",
        tags=["memory", "continuity"],
    )

    results = semantic_search(
        store.capsule,
        "How do agents preserve continuity?",
        limit=1,
    )

    assert len(results) == 1
    assert "continuity" in results[0].memory.text.lower()
