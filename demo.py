"""Runnable continuity transfer demo."""
from capsule.init import new_capsule
from capsule.retrieval import keyword_search
from capsule.store import CapsuleStore


def main() -> None:
    print("Creating source agent capsule...")
    source = new_capsule(owner="Aditya", agent="source-agent", summary="Demo continuity capsule")
    source.add_memory("Aditya is exploring portable memory for AI agents.", kind="project", tags=["memory", "agents"])
    source.add_memory("Keep handoffs inspectable and JSON-first.", kind="principle", tags=["handoff", "json"])
    source.save("capsules/demo_transfer.json")

    print("Loading capsule in receiving agent...")
    receiver = CapsuleStore.load("capsules/demo_transfer.json")
    print(f"Loaded {len(receiver.capsule.memories)} memories for {receiver.capsule.owner}.")

    print("Retrieving handoff context:")
    for memory in keyword_search(receiver.capsule, "agent handoff memory"):
        print(f"- [{memory.kind}] {memory.text}")


if __name__ == "__main__":
    main()
