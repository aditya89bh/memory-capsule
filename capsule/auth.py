"""API-key authentication helpers."""
from __future__ import annotations

import os

from fastapi import Header, HTTPException, status

API_KEY_ENV = "MEMORY_CAPSULE_API_KEY"


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """Require X-API-Key when MEMORY_CAPSULE_API_KEY is configured.

    Auth is disabled by default for local development. Set MEMORY_CAPSULE_API_KEY
    in production to require clients to send X-API-Key.
    """
    expected = os.getenv(API_KEY_ENV)
    if not expected:
        return

    if x_api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
