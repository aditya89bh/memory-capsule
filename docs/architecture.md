# Memory Capsule Architecture

## Core Idea

A memory capsule is a portable continuity object for AI systems.

Instead of trapping memory inside prompts, hidden vector stores, or vendor-specific runtimes, memory is represented as an explicit transferable artifact.

---

## System Overview

```text
                ┌──────────────────────┐
                │      AI Agent A      │
                └──────────┬───────────┘
                           │
                     writes memories
                           │
                           ▼
                ┌──────────────────────┐
                │    Memory Capsule    │
                │  JSON + Embeddings   │
                └──────────┬───────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
   keyword retrieval  semantic search   merge engine
          │                │                │
          └────────────────┼────────────────┘
                           │
                    continuity state
                           │
                           ▼
                ┌──────────────────────┐
                │      AI Agent B      │
                └──────────────────────┘
```

---

## Architecture Components

### 1. Capsule Schema

Defines portable memory structure.

Current objects:

- `MemoryCapsule`
- `MemoryItem`
- metadata
- timestamps
- tags
- memory types

Goals:

- inspectable
- serializable
- versionable
- transferable

---

### 2. Capsule Store

Handles:

- save/load
- memory insertion
- capsule updates
- continuity persistence

Current implementation:

- JSON-backed persistence
- local filesystem storage

Future:

- SQLite backend
- distributed persistence
- cloud sync

---

### 3. Retrieval Layer

Two retrieval modes exist.

#### Keyword Retrieval

Simple token overlap ranking.

Strengths:

- deterministic
- transparent
- fast
- dependency-light

#### Semantic Retrieval

Embedding similarity search using:

- SentenceTransformers
- FAISS

Strengths:

- semantic recall
- flexible matching
- context continuity

Fallback behavior:

If semantic dependencies are unavailable, the system falls back to keyword retrieval.

---

### 4. Merge Engine

Portable continuity becomes useful only when multiple agents can combine memory safely.

The merge engine:

- deduplicates memories
- tracks merge provenance
- reports conflicts
- preserves continuity lineage

Current conflict handling:

- owner mismatch reporting
- duplicate elimination

Future:

- temporal conflict resolution
- trust-weighted merges
- memory priority policies

---

### 5. CLI Layer

Current commands:

```bash
memory-capsule create
memory-capsule add
memory-capsule search
memory-capsule show
```

Future:

```bash
memory-capsule merge
memory-capsule validate
memory-capsule timeline
memory-capsule serve
```

---

## Design Principles

### Human Inspectability

Memory should remain understandable by humans.

### Runtime Portability

Capsules should work across:

- LLM runtimes
- agents
- robots
- orchestration systems

### Graceful Degradation

Advanced features should fail safely.

### Continuity First

The system prioritizes preserving context over maximizing abstraction.

---

## Future Directions

### MCP-Compatible Memory Server

Shared continuity infrastructure for agent ecosystems.

### Streaming Capsules

Real-time continuity updates.

### Memory Timelines

Temporal memory evolution visualization.

### Retention Policies

Short-term vs long-term memory scoring.

### Shared Multi-Agent Capsules

Collaborative memory systems.
