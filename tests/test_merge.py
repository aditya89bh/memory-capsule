from capsule import merge_capsules, new_capsule


def test_capsule_merge_deduplicates_memories():
    left = new_capsule(owner="factory", agent="planner")
    left.add_memory(
        "Reduce insertion speed near the CNC chuck.",
        kind="rule",
        tags=["motion"],
    )

    right = new_capsule(owner="factory", agent="operator")
    right.add_memory(
        "Reduce insertion speed near the CNC chuck.",
        kind="rule",
        tags=["motion"],
    )
    right.add_memory(
        "Operators prefer visual confirmation before cycle start.",
        kind="preference",
        tags=["ux"],
    )

    merged, report = merge_capsules(left.capsule, right.capsule)

    assert len(merged.memories) == 2
    assert report.added == 1
    assert report.skipped_duplicates == 1


def test_owner_conflict_is_reported():
    left = new_capsule(owner="robot-a")
    right = new_capsule(owner="robot-b")

    merged, report = merge_capsules(left.capsule, right.capsule)

    assert merged is not None
    assert report.total_conflicts == 1
