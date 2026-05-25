# memory-capsule

Portable, inspectable memory infrastructure for AI agents.

`memory-capsule` gives agents a transferable continuity object: a structured memory file/store that can move across sessions, models, tools, and runtimes.

## Thesis

Agents should not lose continuity just because the session, model, tool, or runtime changes.

Most agent memory today is either hidden inside prompts, trapped in product-specific databases, or buried in vector stores. `memory-capsule` treats memory as an explicit artifact: readable by humans, usable by agents, and portable across systems.

## What this repo includes

- Pydantic memory capsule schema
- JSON import/export
- CLI for create/add/search/show/validate/migrate
- keyword retrieval
- semantic retrieval with FAISS + SentenceTransformers
- multi-agent handoff demo
- capsule merge + conflict reporting
- validation layer
- schema migration scaffolding
- SQLite persistence backend
- FastAPI service layer
- API-key authentication
- lightweight metrics
- Docker deployment
- CI tests
- retrieval benchmark
- architecture documentation

## Why this matters

A memory capsule gives agents a common continuity artifact:

- human-readable JSON
- explicit schema and timestamps
- import/export across runtimes
- inspectable memory before transfer
- retrieval by keyword or embedding similarity
- mergeable state across multiple agents
- deployable API mode for agent systems

## Architecture

```text
Agent A
  │
  │ writes memories
  ▼
Memory Capsule
  │
  ├── JSON export/import
  ├── SQLite persistence
  ├── keyword retrieval
  ├── semantic retrieval
  ├── validation/migration
  └── merge/conflict reporting
  │
  ▼
Agent B / API / CLI / future MCP server
```

See [`docs/architecture.md`](docs/architecture.md) for the full system overview.

## Quickstart

```bash
git clone https://github.com/aditya89bh/memory-capsule.git
cd memory-capsule
python -m venv .venv
source .venv/bin/activate
pip install -e .
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
memory-capsule validate capsules/demo.json
memory-capsule migrate capsules/demo.json
```

## API Service

Run locally:

```bash
uvicorn capsule.api:app --reload
```

Run with Docker:

```bash
docker compose up
```

Core endpoints:

```text
GET  /health
GET  /metrics
GET  /capsules
POST /capsules
GET  /capsules/{capsule_id}
POST /capsules/{capsule_id}/search
```

Optional API-key auth:

```bash
export MEMORY_CAPSULE_API_KEY="dev-secret"
```

Then send:

```text
X-API-Key: dev-secret
```

## Demos

```bash
python demo.py
python examples/multi_agent_handoff.py
python examples/capsule_merge_demo.py
python examples/semantic_retrieval_demo.py
python benchmarks/continuity_benchmark.py
```

## Minimal Python Usage

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

## Multi-Agent Handoff

```bash
python examples/multi_agent_handoff.py
```

This demonstrates:

1. A source agent exporting structured continuity.
2. A receiving agent loading the capsule.
3. Retrieval of relevant memories.
4. Continuation of work without the original session history.

## Capsule Merge

```bash
python examples/capsule_merge_demo.py
```

This demonstrates:

1. Two agents producing separate memory capsules.
2. Duplicate memory removal.
3. Conflict reporting.
4. Shared continuity state.

## Production Status

This repo is production-oriented, but not yet enterprise-hardened.

Implemented:

- service API
- Docker deployment
- SQLite backend
- API-key auth
- validation
- migrations
- metrics
- logging
- CI

Remaining for serious production deployment:

- full Postgres backend
- async DB pooling
- encryption
- RBAC
- Prometheus/Grafana integration
- MCP-compatible server
- distributed capsule locking
- background embedding jobs

## Roadmap

- [x] Portable capsule schema
- [x] JSON import/export
- [x] CLI
- [x] keyword retrieval
- [x] semantic retrieval
- [x] capsule merge
- [x] validation
- [x] migrations
- [x] SQLite backend
- [x] FastAPI service
- [x] Docker deployment
- [x] API-key auth
- [x] metrics
- [ ] full Postgres backend
- [ ] encryption
- [ ] MCP-compatible memory server
- [ ] dashboard/timeline UI
- [ ] cloud deployment templates

## Positioning

`memory-capsule` is not a chatbot memory toy.

It is a small continuity substrate for agent systems: portable enough to inspect, structured enough to automate, and extensible enough to become shared memory infrastructure.
