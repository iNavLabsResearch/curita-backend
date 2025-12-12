"""
Base service classes for dependency injection and common functionality
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any
from static_memory_cache import StaticMemoryCache
from app.telemetries.logger import logger
from app.core import get_settings

T = TypeVar('T')


class BaseService(ABC):
    """Base service class with common functionality"""
    
    def __init__(self):
        self.settings = get_settings()
        self.logger = logger
    
    @abstractmethod
    def initialize(self):
        """Initialize service resources"""
        pass


class BaseEmbeddingService(BaseService):
    """Base class for embedding services"""
    
    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        pass
    
    @abstractmethod
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        pass
    
    @abstractmethod
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embedding vectors"""
        pass


class BaseDocumentProcessor(BaseService):
    """Base class for document processing"""
    
    @abstractmethod
    def process_document(self, file_bytes: bytes, file_type: str, filename: str) -> List[Dict[str, Any]]:
        """Process document and return chunks with metadata"""
        pass
    
    @abstractmethod
    def extract_text(self, file_bytes: bytes, file_type: str) -> str:
        """Extract text from various file types"""
        pass
    
    @abstractmethod
    def chunk_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Chunk text into smaller pieces"""
        pass


class BaseVectorStorage(BaseService):
    """Base class for vector storage operations"""
    
    @abstractmethod
    async def store_document_chunks(
        self,
        document_id: str,
        chunks: List[Dict[str, Any]],
        embeddings: List[List[float]],
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Store document chunks with embeddings"""
        pass
    
    @abstractmethod
    def get_document_chunks(self, document_id: str) -> List[Dict[str, Any]]:
        """Retrieve all chunks for a document"""
        pass
    
    @abstractmethod
    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """Delete a document and all its chunks"""
        pass
    
    @abstractmethod
    def update_chunk(self, chunk_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a specific chunk"""
        pass
    
    @abstractmethod
    def list_documents(self, limit: int, offset: int) -> List[Dict[str, Any]]:
        """List all documents with pagination"""
        pass


class BaseSearchService(BaseService):
    """Base class for search operations"""
    
    @abstractmethod
    def search(
        self,
        query: str,
        top_k: int,
        similarity_threshold: Optional[float] = None,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Perform semantic search"""
        pass
    
    @abstractmethod
    def search_by_document_id(
        self,
        query: str,
        document_id: str,
        top_k: int
    ) -> List[Dict[str, Any]]:
        """Search within a specific document"""
        pass
