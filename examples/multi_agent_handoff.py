"""Multi-agent handoff demo for memory-capsule."""
from __future__ import annotations

from pathlib import Path

from capsule import CapsuleStore, new_capsule
from capsule.retrieval import keyword_search

OUTPUT_PATH = Path("capsules/project_handoff_capsule.json")


def source_agent_write_capsule() -> Path:
    store = new_capsule(
        owner="memory-capsule-demo",
        agent="source-coding-agent",
        summary="Continuity capsule for a portable memory infrastructure project.",
    )
    store.add_memory(
        "The project thesis is portable, inspectable memory for AI agents.",
        kind="thesis",
        tags=["positioning", "agents", "memory"],
    )
    store.add_memory(
        "The next high-leverage feature is a multi-agent handoff demo.",
        kind="task",
        tags=["demo", "handoff", "priority"],
    )
    store.add_memory(
        "Keep the interface JSON-first so humans can review memory before transfer.",
        kind="principle",
        tags=["json", "trust", "review"],
    )
    store.add_memory(
        "Use simple keyword retrieval first, then add semantic retrieval later.",
        kind="roadmap",
        tags=["retrieval", "semantic-search"],
    )
    return store.save(OUTPUT_PATH)


def receiving_agent_continue(path: Path) -> str:
    store = CapsuleStore.load(path)
    relevant = keyword_search(store.capsule, "handoff demo memory agents", limit=3)

    lines = [
        "Receiving agent loaded capsule continuity:",
        f"owner={store.capsule.owner}",
        f"memories={len(store.capsule.memories)}",
        "",
        "Relevant context:",
    ]
    lines.extend(f"- [{item.kind}] {item.text}" for item in relevant)
    lines.extend(
        [
            "",
            "Next action:",
            "Build and document the multi-agent handoff workflow as the primary demo.",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    capsule_path = source_agent_write_capsule()
    print(receiving_agent_continue(capsule_path))


if __name__ == "__main__":
    main()
