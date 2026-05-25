from capsule.init import new_capsule
from capsule.retrieval import keyword_search

store = new_capsule(owner="Aditya", agent="personal-assistant", summary="Personal assistant continuity")
store.add_memory("Prefers concise status updates with evidence.", kind="preference", tags=["communication"])
store.add_memory("Working on portable memory for AI agents.", kind="project", tags=["memory", "agents"])

for memory in keyword_search(store.capsule, "agent memory"):
    print(f"- {memory.text}")
