"""Optional embedding helpers.

The core project works without embeddings. Install requirements.txt to enable
SentenceTransformers-powered vectors for future semantic retrieval.
"""
from __future__ import annotations

from typing import Iterable

import numpy as np


def embed_texts(texts: Iterable[str], model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> np.ndarray:
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_name)
    return np.asarray(model.encode(list(texts), normalize_embeddings=True))
