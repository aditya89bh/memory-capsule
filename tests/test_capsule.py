from capsule.init import new_capsule
from capsule.retrieval import keyword_search
from capsule.store import CapsuleStore


def test_add_save_load_and_retrieve(tmp_path):
    store = new_capsule(owner="tester", agent="pytest", summary="test capsule")
    store.add_memory("Agents need portable continuity.", tags=["agents", "memory"])
    path = tmp_path / "capsule.json"
    store.save(path)

    loaded = CapsuleStore.load(path)
    assert loaded.capsule.owner == "tester"
    assert len(loaded.capsule.memories) == 1
    assert keyword_search(loaded.capsule, "portable memory")[0].text == "Agents need portable continuity."
