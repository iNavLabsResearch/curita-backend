"""
Embedding service using Snowflake Arctic Embed model.
Provides shared lazy-loaded model + legacy wrapper class.
"""

from typing import List, Optional
import threading

from sentence_transformers import SentenceTransformer

from app.core.config import get_settings
from app.services.base import BaseEmbeddingService
from app.utilities.logger import get_logger

# --------------------------------------------------------------------------- #
# Globals
# --------------------------------------------------------------------------- #
_model: Optional[SentenceTransformer] = None
_model_dim: Optional[int] = None
_logger = get_logger(__name__)
_lock = threading.Lock()


def _load_model() -> SentenceTransformer:
    """Thread-safe lazy load of the embedding model."""
    global _model, _model_dim

    if _model is not None:
        return _model

    with _lock:
        if _model is not None:  # double-checked locking
            return _model

        settings = get_settings()
        model_name = getattr(settings, "EMBEDDING_MODEL", None)
        if not model_name:
            raise ValueError("EMBEDDING_MODEL must be set to the embedding model name.")

        _logger.info(f"Initializing embedding model: {model_name}")

        try:
            _model = SentenceTransformer(
                model_name,
                trust_remote_code=True,   # REQUIRED for Snowflake Arctic
                device="cpu"               # or "cuda" if available
            )

            _model_dim = _model.get_sentence_embedding_dimension()
            _logger.info(f"Embedding model loaded successfully (dim={_model_dim})")

        except Exception:
            _logger.exception("Failed to initialize embedding model.")
            raise

    return _model


def embed(text: str) -> List[float]:
    """Generate embedding for a single text using the shared model."""
    model = _load_model()
    vector = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True,
        truncate="right",
    )
    return vector.tolist()


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for a batch of texts."""
    model = _load_model()
    vectors = model.encode(
        texts,
        convert_to_numpy=True,
        batch_size=32,
        normalize_embeddings=True,
        truncate="right",
    )
    return vectors.tolist()


# --------------------------------------------------------------------------- #
# Legacy-compatible service class
# --------------------------------------------------------------------------- #
class SnowflakeEmbeddingService(BaseEmbeddingService):
    """Service wrapper for generating embeddings via the shared model."""

    def __init__(self):
        super().__init__()
        self.model = _load_model()
        self.embedding_dimension = _model_dim

    def generate_embedding(self, text: str) -> List[float]:
        self.logger.debug(f"Generating embedding (len={len(text)})")
        return embed(text)

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        self.logger.info(f"Batch embedding for {len(texts)} texts")
        return embed_batch(texts)

    def get_embedding_dimension(self) -> int:
        return int(self.embedding_dimension or _model_dim)


# Singleton instance
_embedding_service: Optional[SnowflakeEmbeddingService] = None


def get_embedding_service() -> SnowflakeEmbeddingService:
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = SnowflakeEmbeddingService()
    return _embedding_service
