"""
Initialize services package
"""
from app.services.base import (
    BaseService,
    BaseEmbeddingService,
    BaseDocumentProcessor,
    BaseVectorStorage,
    BaseSearchService,
)
from app.services.document_processor import LangChainDocumentProcessor, get_document_processor
from app.services.embedding_service import SnowflakeEmbeddingService, get_embedding_service
from app.services.vector_storage import SupabaseVectorStorage, get_vector_storage_service
from app.services.search_service import SupabaseSearchService, get_search_service

__all__ = [
    # Base classes
    "BaseService",
    "BaseEmbeddingService",
    "BaseDocumentProcessor",
    "BaseVectorStorage",
    "BaseSearchService",
    # Implementations
    "LangChainDocumentProcessor",
    "get_document_processor",
    "SnowflakeEmbeddingService",
    "get_embedding_service",
    "SupabaseVectorStorage",
    "get_vector_storage_service",
    "SupabaseSearchService",
    "get_search_service",
]
