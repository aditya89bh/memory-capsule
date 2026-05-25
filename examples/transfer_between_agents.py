from capsule.store import CapsuleStore
from capsule.retrieval import keyword_search

sender = CapsuleStore.load("capsules/user_capsule.json")
sender.add_memory("The receiving agent should preserve project context across handoff.", tags=["handoff"])
sender.save("capsules/transferred_capsule.json")

receiver = CapsuleStore.load("capsules/transferred_capsule.json")
print("Receiver loaded:", receiver.capsule.owner)
for item in keyword_search(receiver.capsule, "handoff project"):
    print("-", item.text)
