"""
CRUD operations for Memory entities (Toy Memory and Agent Memory).
Provides database operations for managing memory storage in the system.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from app.data_layer.crud.base_crud import BaseCRUD
from app.data_layer.data_classes.memory_schemas import (
    ToyMemoryCreate,
    ToyMemoryUpdate,
    ToyMemoryResponse,
    AgentMemoryCreate,
    AgentMemoryUpdate,
    AgentMemoryResponse
)
from app.data_layer.supabase_client import SupabaseClient
from app.telemetries.logger import logger


# ============================================================================
# TOY MEMORY CRUD
# ============================================================================

class ToyMemoryCRUD(BaseCRUD[ToyMemoryCreate, ToyMemoryUpdate, ToyMemoryResponse]):
    """
    CRUD operations for Toy Memory entities.
    
    Handles all database operations related to toy memory including:
    - Basic CRUD operations (inherited from BaseCRUD)
    - Queries by toy_id
    - Content type filtering
    - Embedding-based similarity search
    """
    
    def __init__(self, supabase_client: Optional[SupabaseClient] = None):
        """
        Initialize ToyMemoryCRUD instance.
        
        Args:
            supabase_client: Optional Supabase client instance
        """
        super().__init__(
            table_name="toy_memory",
            response_model=ToyMemoryResponse,
            supabase_client=supabase_client
        )
    
    async def get_by_toy_id(
        self,
        toy_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[ToyMemoryResponse]:
        """
        Retrieve all memory records for a specific toy.
        
        Args:
            toy_id: UUID of the toy
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of toy memory records
        """
        try:
            logger.debug(f"Fetching toy memory for toy_id: {toy_id}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"toy_id": str(toy_id)},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching toy memory for toy_id {toy_id}: {str(e)}", exc_info=True)
            return []
    
    async def get_by_content_type(
        self,
        content_type: str,
        toy_id: Optional[UUID] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[ToyMemoryResponse]:
        """
        Retrieve memory records by content type.
        
        Args:
            content_type: Type of content (e.g., 'conversation', 'document')
            toy_id: Optional UUID of toy to filter by
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of matching toy memory records
        """
        try:
            logger.debug(f"Fetching toy memory for content_type: {content_type}")
            
            filters = {"content_type": content_type}
            if toy_id:
                filters["toy_id"] = str(toy_id)
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters=filters,
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching toy memory for content_type {content_type}: {str(e)}", exc_info=True)
            return []
    
    async def search_by_embedding(
        self,
        embedding_vector: List[float],
        toy_id: Optional[UUID] = None,
        limit: int = 10,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search for similar memory records using embedding vectors.
        
        This method uses PostgreSQL RPC function for vector similarity search.
        Note: Requires pgvector extension and appropriate RPC function in database.
        
        Args:
            embedding_vector: Query embedding vector (384 dimensions)
            toy_id: Optional UUID of toy to filter by
            limit: Maximum number of results to return
            similarity_threshold: Minimum similarity score (0-1)
            
        Returns:
            List of matching records with similarity scores
        """
        try:
            logger.debug(f"Searching toy memory by embedding (toy_id: {toy_id}, limit: {limit})")
            
            # Prepare RPC function parameters
            params = {
                "query_embedding": embedding_vector,
                "match_threshold": similarity_threshold,
                "match_count": limit
            }
            
            if toy_id:
                params["filter_toy_id"] = str(toy_id)
            
            # Call RPC function for similarity search
            # Note: This requires a database function like 'search_toy_memory'
            result = await self.supabase.call_rpc_function(
                "search_toy_memory",
                params
            )
            
            if result:
                logger.info(f"Found {len(result)} similar toy memory records")
                return result
            
            logger.info("No similar toy memory records found")
            return []
            
        except Exception as e:
            logger.error(f"Error searching toy memory by embedding: {str(e)}", exc_info=True)
            return []
    
    async def delete_by_toy_id(self, toy_id: UUID) -> bool:
        """
        Delete all memory records for a specific toy.
        
        Args:
            toy_id: UUID of the toy
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            logger.debug(f"Deleting all toy memory for toy_id: {toy_id}")
            
            result = await self.supabase.delete(
                self.table_name,
                filters={"toy_id": str(toy_id)}
            )
            
            if result:
                logger.info(f"Successfully deleted toy memory for toy_id: {toy_id}")
                return True
            
            logger.warning(f"Failed to delete toy memory for toy_id: {toy_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error deleting toy memory for toy_id {toy_id}: {str(e)}", exc_info=True)
            return False


# ============================================================================
# AGENT MEMORY CRUD
# ============================================================================

class AgentMemoryCRUD(BaseCRUD[AgentMemoryCreate, AgentMemoryUpdate, AgentMemoryResponse]):
    """
    CRUD operations for Agent Memory entities.
    
    Handles all database operations related to agent memory including:
    - Basic CRUD operations (inherited from BaseCRUD)
    - Queries by agent_id and toy_id
    - File-based filtering
    - Embedding-based similarity search
    """
    
    def __init__(self, supabase_client: Optional[SupabaseClient] = None):
        """
        Initialize AgentMemoryCRUD instance.
        
        Args:
            supabase_client: Optional Supabase client instance
        """
        super().__init__(
            table_name="agent_memory",
            response_model=AgentMemoryResponse,
            supabase_client=supabase_client
        )
    
    async def get_by_agent_id(
        self,
        agent_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[AgentMemoryResponse]:
        """
        Retrieve all memory records for a specific agent.
        
        Args:
            agent_id: UUID of the agent
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of agent memory records
        """
        try:
            logger.debug(f"Fetching agent memory for agent_id: {agent_id}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"agent_id": str(agent_id)},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching agent memory for agent_id {agent_id}: {str(e)}", exc_info=True)
            return []
    
    async def get_by_toy_id(
        self,
        toy_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[AgentMemoryResponse]:
        """
        Retrieve all memory records for a specific toy.
        
        Args:
            toy_id: UUID of the toy
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of agent memory records
        """
        try:
            logger.debug(f"Fetching agent memory for toy_id: {toy_id}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"toy_id": str(toy_id)},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching agent memory for toy_id {toy_id}: {str(e)}", exc_info=True)
            return []
    
    async def get_by_storage_file_id(
        self,
        storage_file_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[AgentMemoryResponse]:
        """
        Retrieve all memory chunks for a specific file.
        
        Args:
            storage_file_id: Storage file identifier
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of agent memory records for the file
        """
        try:
            logger.debug(f"Fetching agent memory for storage_file_id: {storage_file_id}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"storage_file_id": storage_file_id},
                order_by="chunk_index",
                order_desc=False
            )
            
        except Exception as e:
            logger.error(f"Error fetching agent memory for storage_file_id {storage_file_id}: {str(e)}", exc_info=True)
            return []
    
    async def get_by_content_type(
        self,
        content_type: str,
        agent_id: Optional[UUID] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[AgentMemoryResponse]:
        """
        Retrieve memory records by content type.
        
        Args:
            content_type: MIME type of content
            agent_id: Optional UUID of agent to filter by
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of matching agent memory records
        """
        try:
            logger.debug(f"Fetching agent memory for content_type: {content_type}")
            
            filters = {"content_type": content_type}
            if agent_id:
                filters["agent_id"] = str(agent_id)
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters=filters,
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching agent memory for content_type {content_type}: {str(e)}", exc_info=True)
            return []
    
    async def search_by_embedding(
        self,
        embedding_vector: List[float],
        agent_id: Optional[UUID] = None,
        toy_id: Optional[UUID] = None,
        limit: int = 10,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search for similar memory records using embedding vectors.
        
        This method uses PostgreSQL RPC function for vector similarity search.
        Note: Requires pgvector extension and appropriate RPC function in database.
        
        Args:
            embedding_vector: Query embedding vector (384 dimensions)
            agent_id: Optional UUID of agent to filter by
            toy_id: Optional UUID of toy to filter by
            limit: Maximum number of results to return
            similarity_threshold: Minimum similarity score (0-1)
            
        Returns:
            List of matching records with similarity scores
        """
        try:
            logger.debug(f"Searching agent memory by embedding (agent_id: {agent_id}, toy_id: {toy_id}, limit: {limit})")
            
            # Prepare RPC function parameters
            params = {
                "query_embedding": embedding_vector,
                "match_threshold": similarity_threshold,
                "match_count": limit
            }
            
            if agent_id:
                params["filter_agent_id"] = str(agent_id)
            if toy_id:
                params["filter_toy_id"] = str(toy_id)
            
            # Call RPC function for similarity search
            # Note: This requires a database function like 'search_agent_memory'
            result = await self.supabase.call_rpc_function(
                "search_agent_memory",
                params
            )
            
            if result:
                logger.info(f"Found {len(result)} similar agent memory records")
                return result
            
            logger.info("No similar agent memory records found")
            return []
            
        except Exception as e:
            logger.error(f"Error searching agent memory by embedding: {str(e)}", exc_info=True)
            return []
    
    async def delete_by_agent_id(self, agent_id: UUID) -> bool:
        """
        Delete all memory records for a specific agent.
        
        Args:
            agent_id: UUID of the agent
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            logger.debug(f"Deleting all agent memory for agent_id: {agent_id}")
            
            result = await self.supabase.delete(
                self.table_name,
                filters={"agent_id": str(agent_id)}
            )
            
            if result:
                logger.info(f"Successfully deleted agent memory for agent_id: {agent_id}")
                return True
            
            logger.warning(f"Failed to delete agent memory for agent_id: {agent_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error deleting agent memory for agent_id {agent_id}: {str(e)}", exc_info=True)
            return False
    
    async def delete_by_storage_file_id(self, storage_file_id: str) -> bool:
        """
        Delete all memory chunks for a specific file.
        
        Args:
            storage_file_id: Storage file identifier
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            logger.debug(f"Deleting all agent memory for storage_file_id: {storage_file_id}")
            
            result = await self.supabase.delete(
                self.table_name,
                filters={"storage_file_id": storage_file_id}
            )
            
            if result:
                logger.info(f"Successfully deleted agent memory for storage_file_id: {storage_file_id}")
                return True
            
            logger.warning(f"Failed to delete agent memory for storage_file_id: {storage_file_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error deleting agent memory for storage_file_id {storage_file_id}: {str(e)}", exc_info=True)
            return False


# ============================================================================
# SINGLETON INSTANCES
# ============================================================================

_toy_memory_crud_instance: Optional[ToyMemoryCRUD] = None
_agent_memory_crud_instance: Optional[AgentMemoryCRUD] = None


def get_toy_memory_crud() -> ToyMemoryCRUD:
    """Get or create the singleton ToyMemoryCRUD instance."""
    global _toy_memory_crud_instance
    if _toy_memory_crud_instance is None:
        _toy_memory_crud_instance = ToyMemoryCRUD()
    return _toy_memory_crud_instance


def get_agent_memory_crud() -> AgentMemoryCRUD:
    """Get or create the singleton AgentMemoryCRUD instance."""
    global _agent_memory_crud_instance
    if _agent_memory_crud_instance is None:
        _agent_memory_crud_instance = AgentMemoryCRUD()
    return _agent_memory_crud_instance
