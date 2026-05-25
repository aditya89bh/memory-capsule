"""FastAPI service for memory-capsule."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .retrieval import keyword_search
from .schema import MemoryCapsule
from .sqlite_backend import SQLiteStorageBackend

app = FastAPI(title="memory-capsule", version="0.2.0")
backend = SQLiteStorageBackend()


class SearchRequest(BaseModel):
    query: str
    limit: int = 5


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


@app.get("/capsules")
def list_capsules():
    return {"capsules": list(backend.list_capsules())}


@app.post("/capsules")
def create_capsule(capsule: MemoryCapsule):
    backend.save_capsule(capsule)
    return {
        "status": "saved",
        "capsule_id": capsule.capsule_id,
    }


@app.get("/capsules/{capsule_id}")
def get_capsule(capsule_id: str):
    try:
        capsule = backend.load_capsule(capsule_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return capsule.model_dump(mode="json")


@app.post("/capsules/{capsule_id}/search")
def search_capsule(capsule_id: str, request: SearchRequest):
    try:
        capsule = backend.load_capsule(capsule_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    results = keyword_search(capsule, request.query, limit=request.limit)

    return {
        "query": request.query,
        "results": [memory.model_dump(mode="json") for memory in results],
    }
