# memory-capsule

Portable memory file and store for AI agents.

## Thesis

AI agents need continuity that is portable, inspectable, and easy to hand off. `memory-capsule` treats memory as a small JSON capsule: structured enough for tools, simple enough for humans, and independent of any one agent runtime.

## Why this matters

Most agent memory is trapped inside a product, prompt, database, or hidden vector store. That makes it hard to migrate agents, audit what they know, or transfer context safely between assistants, coding agents, robots, and evaluation systems.

A memory capsule gives agents a common memory artifact:

- human-readable JSON
- explicit schema and timestamps
- import/export across runtimes
- retrieval that can start simple and grow toward embeddings
- safer handoffs because memory can be reviewed before transfer

## Architecture overview

```text
capsule/
  schema.py       Pydantic models for MemoryItem and MemoryCapsule
  store.py        Add, load, and save memories
  retrieval.py    Keyword retrieval over text, tags, and kind
  serializer.py   JSON import/export helpers
  embeddings.py   Optional SentenceTransformers embedding helper
  cli.py          Command line interface
```

Data flow:

1. Create a `MemoryCapsule` for an owner/agent.
2. Add `MemoryItem` entries as preferences, facts, project notes, or safety rules.
3. Save the capsule as JSON.
4. Import it in another agent.
5. Retrieve relevant memory by keyword today; add semantic retrieval tomorrow.

## Example capsule JSON

```json
{
  "capsule_id": "user-capsule-demo",
  "owner": "Aditya",
  "agent": "personal-assistant",
  "version": "0.1.0",
  "summary": "Portable user preferences and project continuity for agent handoffs.",
  "memories": [
    {
      "id": "mem-user-001",
      "text": "Aditya prefers concise, action-oriented updates with concrete evidence.",
      "kind": "preference",
      "tags": ["communication", "updates"],
      "metadata": {"source": "sample"},
      "created_at": "2026-05-25T00:00:00Z"
    }
  ],
  "metadata": {"example": true},
  "updated_at": "2026-05-25T00:02:00Z"
}
```

## Quickstart

```bash
git clone https://github.com/aditya89bh/memory-capsule.git
cd memory-capsule
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python demo.py
```

## CLI Usage

```bash
memory-capsule create capsules/demo.json --owner Aditya

memory-capsule add capsules/demo.json \
  "Robots should preserve operational continuity" \
  --kind principle \
  --tag robotics

memory-capsule search capsules/demo.json continuity

memory-capsule show capsules/demo.json --pretty
```

## Multi-Agent Handoff Demo

```bash
python examples/multi_agent_handoff.py
```

This demonstrates:

1. A source agent exporting structured continuity.
2. A receiving agent loading the capsule.
3. Retrieval of relevant memories.
4. Continuation of work without the original session history.

## Minimal Usage

```python
from capsule import new_capsule
from capsule.retrieval import keyword_search

store = new_capsule(owner="Ada", agent="assistant")
store.add_memory(
    "Ada prefers short answers with examples.",
    kind="preference",
    tags=["style"],
)
store.save("capsules/ada_capsule.json")

results = keyword_search(store.capsule, "short style")
print(results[0].text)
```

## Roadmap

- [ ] Semantic retrieval with FAISS indexes
- [ ] Capsule merge and conflict resolution
- [ ] Memory privacy labels and redaction helpers
- [ ] Agent-to-agent transfer protocol examples
- [ ] CLI for validating and querying capsule files
- [ ] Versioned schema migrations
- [ ] Optional encryption for sensitive capsules
- [ ] Shared capsules across multiple agents
