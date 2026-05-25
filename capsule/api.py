"""FastAPI service for memory-capsule."""
from __future__ import annotations

import logging

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from .auth import require_api_key
from .logging_utils import configure_logging
from .metrics import increment, snapshot
from .retrieval import keyword_search
from .schema import MemoryCapsule
from .sqlite_backend import SQLiteStorageBackend

configure_logging()
logger = logging.getLogger("memory-capsule.api")

app = FastAPI(title="memory-capsule", version="0.3.0")
backend = SQLiteStorageBackend()


class SearchRequest(BaseModel):
    query: str
    limit: int = 5


@app.get("/health")
def healthcheck():
    increment("health_requests")
    logger.info("healthcheck requested")
    return {"status": "ok"}


@app.get("/metrics")
def metrics(_: None = Depends(require_api_key)):
    increment("metrics_requests")
    return snapshot()


@app.get("/capsules")
def list_capsules(_: None = Depends(require_api_key)):
    capsules = list(backend.list_capsules())
    increment("list_capsules_requests")
    logger.info("listing capsules", extra={"count": len(capsules)})
    return {"capsules": capsules}


@app.post("/capsules")
def create_capsule(capsule: MemoryCapsule, _: None = Depends(require_api_key)):
    backend.save_capsule(capsule)
    increment("create_capsule_requests")
    logger.info(
        "capsule saved",
        extra={
            "capsule_id": capsule.capsule_id,
            "owner": capsule.owner,
        },
    )
    return {
        "status": "saved",
        "capsule_id": capsule.capsule_id,
    }


@app.get("/capsules/{capsule_id}")
def get_capsule(capsule_id: str, _: None = Depends(require_api_key)):
    try:
        capsule = backend.load_capsule(capsule_id)
    except KeyError as exc:
        increment("get_capsule_failures")
        logger.warning("capsule lookup failed", extra={"capsule_id": capsule_id})
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    increment("get_capsule_requests")
    logger.info("capsule loaded", extra={"capsule_id": capsule_id})
    return capsule.model_dump(mode="json")


@app.post("/capsules/{capsule_id}/search")
def search_capsule(capsule_id: str, request: SearchRequest, _: None = Depends(require_api_key)):
    try:
        capsule = backend.load_capsule(capsule_id)
    except KeyError as exc:
        increment("search_failures")
        logger.warning("search failed", extra={"capsule_id": capsule_id})
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    results = keyword_search(capsule, request.query, limit=request.limit)

    increment("search_requests")
    logger.info(
        "search completed",
        extra={
            "capsule_id": capsule_id,
            "query": request.query,
            "results": len(results),
        },
    )

    return {
        "query": request.query,
        "results": [memory.model_dump(mode="json") for memory in results],
    }
