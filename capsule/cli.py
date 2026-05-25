"""Command line interface for memory-capsule."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .init import new_capsule
from .migrations import CURRENT_SCHEMA_VERSION, migrate_payload
from .retrieval import keyword_search
from .serializer import import_capsule
from .store import CapsuleStore
from .validation import validate_capsule


def _load_or_create(path: Path, owner: str = "unknown", agent: str | None = None) -> CapsuleStore:
    if path.exists():
        return CapsuleStore.load(path)
    return new_capsule(owner=owner, agent=agent)


def create_capsule(args: argparse.Namespace) -> None:
    store = new_capsule(owner=args.owner, agent=args.agent, summary=args.summary)
    output = store.save(args.path)
    print(f"Created capsule: {output}")


def add_memory(args: argparse.Namespace) -> None:
    path = Path(args.path)
    store = _load_or_create(path, owner=args.owner, agent=args.agent)
    memory = store.add_memory(args.text, kind=args.kind, tags=args.tags or [])
    store.save(path)
    print(f"Added memory {memory.id} to {path}")


def search_capsule(args: argparse.Namespace) -> None:
    store = CapsuleStore.load(args.path)
    results = keyword_search(store.capsule, args.query, limit=args.limit)
    if not results:
        print("No matching memories found.")
        return
    for index, item in enumerate(results, start=1):
        tags = ", ".join(item.tags) if item.tags else "no-tags"
        print(f"{index}. [{item.kind}] {item.text} ({tags})")


def show_capsule(args: argparse.Namespace) -> None:
    store = CapsuleStore.load(args.path)
    data = store.capsule.model_dump(mode="json")
    if args.pretty:
        print(json.dumps(data, indent=2))
        return
    print(f"Capsule: {store.capsule.capsule_id}")
    print(f"Owner: {store.capsule.owner}")
    print(f"Agent: {store.capsule.agent}")
    print(f"Memories: {len(store.capsule.memories)}")
    if store.capsule.summary:
        print(f"Summary: {store.capsule.summary}")


def validate_capsule_command(args: argparse.Namespace) -> None:
    capsule = import_capsule(args.path)
    report = validate_capsule(capsule)

    print(f"valid: {report.valid}")

    if report.errors:
        print("errors:")
        for error in report.errors:
            print(f"- {error}")

    if report.warnings:
        print("warnings:")
        for warning in report.warnings:
            print(f"- {warning}")


def migrate_capsule_command(args: argparse.Namespace) -> None:
    payload = json.loads(Path(args.path).read_text(encoding="utf-8"))
    migrated = migrate_payload(payload, target_version=CURRENT_SCHEMA_VERSION)

    output_path = Path(args.output or args.path)
    output_path.write_text(json.dumps(migrated, indent=2), encoding="utf-8")

    print(f"Migrated capsule to version {CURRENT_SCHEMA_VERSION}")
    print(f"Output: {output_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="memory-capsule",
        description="Create, inspect, and query portable memory capsules for AI agents.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="Create a new empty capsule JSON file.")
    create.add_argument("path", type=Path, help="Output path for the capsule JSON file.")
    create.add_argument("--owner", required=True, help="Human, agent, team, or system that owns the capsule.")
    create.add_argument("--agent", default=None, help="Agent/runtime that created the capsule.")
    create.add_argument("--summary", default="", help="Short capsule summary.")
    create.set_defaults(func=create_capsule)

    add = subparsers.add_parser("add", help="Add a memory to a capsule file.")
    add.add_argument("path", type=Path, help="Capsule JSON path. Created if missing.")
    add.add_argument("text", help="Memory text to store.")
    add.add_argument("--kind", default="note", help="Memory type, e.g. preference, fact, project, rule.")
    add.add_argument("--tag", dest="tags", action="append", help="Repeatable tag for the memory.")
    add.add_argument("--owner", default="unknown", help="Owner used only if the capsule file does not exist.")
    add.add_argument("--agent", default=None, help="Agent used only if the capsule file does not exist.")
    add.set_defaults(func=add_memory)

    search = subparsers.add_parser("search", help="Search memories by keyword overlap.")
    search.add_argument("path", type=Path, help="Capsule JSON path.")
    search.add_argument("query", help="Search query.")
    search.add_argument("--limit", type=int, default=5, help="Maximum number of results.")
    search.set_defaults(func=search_capsule)

    show = subparsers.add_parser("show", help="Show capsule metadata or raw JSON.")
    show.add_argument("path", type=Path, help="Capsule JSON path.")
    show.add_argument("--pretty", action="store_true", help="Print full formatted JSON.")
    show.set_defaults(func=show_capsule)

    validate = subparsers.add_parser("validate", help="Validate a capsule file.")
    validate.add_argument("path", type=Path, help="Capsule JSON path.")
    validate.set_defaults(func=validate_capsule_command)

    migrate = subparsers.add_parser("migrate", help="Migrate a capsule schema version.")
    migrate.add_argument("path", type=Path, help="Capsule JSON path.")
    migrate.add_argument("--output", default=None, help="Optional output path.")
    migrate.set_defaults(func=migrate_capsule_command)

    return parser


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
