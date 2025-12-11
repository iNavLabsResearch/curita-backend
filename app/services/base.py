"""
Base service classes for dependency injection and common functionality
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from static_memory_cache import StaticMemoryCache
from app.telemetries.logger import logger


class BaseService(ABC):
    """
    Base service class with common functionality
    All services should inherit from this class
    """
    
    def __init__(self):
        """Initialize base service with settings and logger"""
        self.settings = StaticMemoryCache
        self.logger = logger
        self._initialized = False
    
    async def initialize(self):
        """
        Initialize service resources (async)
        Override this method in subclasses for async initialization
        """
        if self._initialized:
            return
        self._initialized = True


class BaseDatabaseService(BaseService):
    """
    Base class for services that interact with Supabase database
    Provides common Supabase client initialization
    """
    
    def __init__(self, table_name: Optional[str] = None):
        """
        Initialize database service
        
        Args:
            table_name: Optional table name for this service
        """
        super().__init__()
        self.table_name = table_name
        self.supabase = None
    
    async def initialize(self):
        """Initialize Supabase client"""
        if self._initialized:
            return
        
        from app.data_layer.supabase_client import get_supabase
        self.supabase = await get_supabase()
        self._initialized = True
        
        if self.table_name:
            self.logger.info(f"{self.__class__.__name__} initialized for table: {self.table_name}")
        else:
            self.logger.info(f"{self.__class__.__name__} initialized")


class BaseMemoryService(BaseDatabaseService):
    """
    Base class for memory services (toy_memory, agent_memory, conversation_logs)
    Provides common memory storage patterns with embeddings
    """
    
    def __init__(self, table_name: str):
        """
        Initialize memory service
        
        Args:
            table_name: Table name for storing memory records
        """
        super().__init__(table_name)
        self.embedding_service = None
    
    async def initialize(self):
        """Initialize database and embedding service"""
        if self._initialized:
            return
        
        await super().initialize()
        
        from app.services.embedding_service import get_embedding_service
        self.embedding_service = get_embedding_service()
        
        self._initialized = True
        self.logger.info(f"{self.__class__.__name__} fully initialized with embeddings")
    
    @abstractmethod
    async def store_with_embeddings(
        self,
        text_chunks: List[str],
        metadata: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Store text chunks with their embeddings
        
        Args:
            text_chunks: List of text chunks to store
            metadata: Metadata for the chunks
            
        Returns:
            List of stored records
        """
        pass
    
    @abstractmethod
    async def search_similar(
        self,
        query_text: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar memories using vector similarity
        
        Args:
            query_text: Query text for similarity search
            limit: Maximum number of results
            filters: Optional filters for search
            
        Returns:
            List of similar records
        """
        pass


class BaseEmbeddingService(BaseService):
    """Base class for embedding generation services"""
    
    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector as list of floats
        """
        pass
    
    @abstractmethod
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (batch operation)
        
        Args:
            texts: List of input texts
            
        Returns:
            List of embedding vectors
        """
        pass
    
    @abstractmethod
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embedding vectors
        
        Returns:
            Dimension size
        """
        pass


class BaseChunkingService(BaseService):
    """Base class for text chunking services"""
    
    @abstractmethod
    def chunk_text(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Chunk text into smaller pieces
        
        Args:
            text: Input text to chunk
            metadata: Optional metadata to attach to chunks
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        pass
    
    @abstractmethod
    def get_chunk_statistics(
        self,
        chunks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Get statistics about chunks
        
        Args:
            chunks: List of chunk dictionaries
            
        Returns:
            Dictionary with statistics (total_chunks, avg_size, etc.)
        """
        pass
