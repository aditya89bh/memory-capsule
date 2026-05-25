"""Demonstrate merging continuity from multiple agents."""
from __future__ import annotations

from capsule import new_capsule
from capsule.merge import merge_capsules


def build_agent_capsules():
    planner = new_capsule(
        owner="factory-cell",
        agent="planner-agent",
        summary="Planning continuity for robotic operations.",
    )
    planner.add_memory(
        "Tray alignment drift appears after long production cycles.",
        kind="observation",
        tags=["robotics", "alignment"],
    )
    planner.add_memory(
        "Reduce insertion speed near the CNC chuck.",
        kind="rule",
        tags=["safety", "motion"],
    )

    operator = new_capsule(
        owner="factory-cell",
        agent="operator-agent",
        summary="Operational continuity from shift handoff.",
    )
    operator.add_memory(
        "Reduce insertion speed near the CNC chuck.",
        kind="rule",
        tags=["safety", "motion"],
    )
    operator.add_memory(
        "Operators prefer visual confirmation before cycle start.",
        kind="preference",
        tags=["ux", "workflow"],
    )

    return planner.capsule, operator.capsule


def main() -> None:
    planner, operator = build_agent_capsules()

    merged, report = merge_capsules(planner, operator)

    print("Merged capsule summary")
    print("----------------------")
    print(f"owner: {merged.owner}")
    print(f"total memories: {len(merged.memories)}")
    print(f"added memories: {report.added}")
    print(f"duplicates skipped: {report.skipped_duplicates}")
    print(f"conflicts: {report.total_conflicts}")
    print()

    for memory in merged.memories:
        print(f"- [{memory.kind}] {memory.text}")


if __name__ == "__main__":
    main()
