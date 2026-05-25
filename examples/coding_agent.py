from capsule.init import new_capsule

store = new_capsule(owner="developer", agent="coding-agent")
store.add_memory("Use one task per commit and run tests before pushing.", kind="workflow", tags=["git", "tests"])
store.save("capsules/coding_agent_capsule.json")
print("Saved capsules/coding_agent_capsule.json")
