"""
CRUD operations for Memory (Toy Memory and Agent Memory)
"""
from uuid import UUID
from typing import List, Optional
from app.data_layer.supabase_client import SupabaseClient
from app.data_layer.crud.base_crud import BaseCrud
from app.data_layer.data_classes.memory_schemas import (
    ToyMemoryResponse,
    AgentMemoryResponse,
)
from app.telemetries.logger import logger


class ToyMemoryCRUD(BaseCrud):
    """CRUD operations for toy_memory table"""
    
    def __init__(self, supabase: SupabaseClient):
        super().__init__(supabase, "toy_memory", ToyMemoryResponse)
    
    async def get_memories_by_toy(self, toy_id: UUID) -> List[ToyMemoryResponse]:
        """
        Get all memories for a specific toy
        
        Args:
            toy_id: UUID of the toy
            
        Returns:
            List of toy memory records
        """
        try:
            logger.debug(f"Fetching memories for toy {toy_id}")
            return await self.filter_by(toy_id=str(toy_id))
        except Exception as e:
            logger.error(f"Error fetching memories for toy {toy_id}: {str(e)}")
            raise
    
    async def get_memories_by_content_type(self, toy_id: UUID, content_type: str) -> List[ToyMemoryResponse]:
        """
        Get memories by content type for a specific toy
        
        Args:
            toy_id: UUID of the toy
            content_type: Type of content
            
        Returns:
            List of toy memory records
        """
        try:
            logger.debug(f"Fetching memories for toy {toy_id} with content type {content_type}")
            return await self.filter_by(toy_id=str(toy_id), content_type=content_type)
        except Exception as e:
            logger.error(f"Error fetching memories by content type: {str(e)}")
            raise
    
    async def get_memories_by_chunk_index(self, toy_id: UUID, chunk_index: int) -> List[ToyMemoryResponse]:
        """
        Get memories by chunk index for a specific toy
        
        Args:
            toy_id: UUID of the toy
            chunk_index: Index of the chunk
            
        Returns:
            List of toy memory records
        """
        try:
            logger.debug(f"Fetching memories for toy {toy_id} with chunk index {chunk_index}")
            return await self.filter_by(toy_id=str(toy_id), chunk_index=chunk_index)
        except Exception as e:
            logger.error(f"Error fetching memories by chunk index: {str(e)}")
            raise
    
    async def vector_search(
        self, 
        toy_id: UUID, 
        embedding_vector: List[float], 
        limit: int = 5,
        similarity_threshold: Optional[float] = None
    ) -> List[dict]:
        """
        Perform vector similarity search on toy memory
        
        Args:
            toy_id: UUID of the toy
            embedding_vector: Vector embedding to search for
            limit: Maximum number of results
            similarity_threshold: Minimum similarity score (optional)
            
        Returns:
            List of memory records with similarity scores
        """
        try:
            logger.debug(f"Performing vector search for toy {toy_id}")
            # Note: This requires pgvector extension and proper setup
            # The actual implementation depends on Supabase's vector search capabilities
            query = await self.supabase.table(self.table_name).select("*").eq("toy_id", str(toy_id)).execute()
            
            # Vector search would typically use a custom RPC function
            # For now, we'll return a basic query structure
            # In production, you'd call an RPC function like:
            # result = await self.supabase.rpc('search_toy_memory', {
            #     'toy_id': str(toy_id),
            #     'query_embedding': embedding_vector,
            #     'match_threshold': similarity_threshold or 0.5,
            #     'match_count': limit
            # }).execute()
            
            logger.warning("Vector search not fully implemented. Requires RPC function setup.")
            return []
        except Exception as e:
            logger.error(f"Error performing vector search: {str(e)}")
            raise


class AgentMemoryCRUD(BaseCrud):
    """CRUD operations for agent_memory table"""
    
    def __init__(self, supabase: SupabaseClient):
        super().__init__(supabase, "agent_memory", AgentMemoryResponse)
    
    async def get_memories_by_agent(self, agent_id: UUID) -> List[AgentMemoryResponse]:
        """
        Get all memories for a specific agent
        
        Args:
            agent_id: UUID of the agent
            
        Returns:
            List of agent memory records
        """
        try:
            logger.debug(f"Fetching memories for agent {agent_id}")
            return await self.filter_by(agent_id=str(agent_id))
        except Exception as e:
            logger.error(f"Error fetching memories for agent {agent_id}: {str(e)}")
            raise
    
    async def get_memories_by_toy(self, toy_id: UUID) -> List[AgentMemoryResponse]:
        """
        Get all memories for a specific toy
        
        Args:
            toy_id: UUID of the toy
            
        Returns:
            List of agent memory records
        """
        try:
            logger.debug(f"Fetching memories for toy {toy_id}")
            return await self.filter_by(toy_id=str(toy_id))
        except Exception as e:
            logger.error(f"Error fetching memories for toy {toy_id}: {str(e)}")
            raise
    
    async def get_memories_by_agent_and_toy(self, agent_id: UUID, toy_id: UUID) -> List[AgentMemoryResponse]:
        """
        Get all memories for a specific agent and toy
        
        Args:
            agent_id: UUID of the agent
            toy_id: UUID of the toy
            
        Returns:
            List of agent memory records
        """
        try:
            logger.debug(f"Fetching memories for agent {agent_id} and toy {toy_id}")
            return await self.filter_by(agent_id=str(agent_id), toy_id=str(toy_id))
        except Exception as e:
            logger.error(f"Error fetching memories for agent and toy: {str(e)}")
            raise
    
    async def get_memories_by_filename(self, agent_id: UUID, filename: str) -> List[AgentMemoryResponse]:
        """
        Get memories by original filename
        
        Args:
            agent_id: UUID of the agent
            filename: Original filename
            
        Returns:
            List of agent memory records
        """
        try:
            logger.debug(f"Fetching memories for agent {agent_id} with filename {filename}")
            return await self.filter_by(agent_id=str(agent_id), original_filename=filename)
        except Exception as e:
            logger.error(f"Error fetching memories by filename: {str(e)}")
            raise
    
    async def get_memories_by_content_type(self, agent_id: UUID, content_type: str) -> List[AgentMemoryResponse]:
        """
        Get memories by content type for a specific agent
        
        Args:
            agent_id: UUID of the agent
            content_type: Type of content
            
        Returns:
            List of agent memory records
        """
        try:
            logger.debug(f"Fetching memories for agent {agent_id} with content type {content_type}")
            return await self.filter_by(agent_id=str(agent_id), content_type=content_type)
        except Exception as e:
            logger.error(f"Error fetching memories by content type: {str(e)}")
            raise
    
    async def vector_search(
        self, 
        agent_id: UUID, 
        embedding_vector: List[float], 
        limit: int = 5,
        similarity_threshold: Optional[float] = None
    ) -> List[dict]:
        """
        Perform vector similarity search on agent memory
        
        Args:
            agent_id: UUID of the agent
            embedding_vector: Vector embedding to search for
            limit: Maximum number of results
            similarity_threshold: Minimum similarity score (optional)
            
        Returns:
            List of memory records with similarity scores
        """
        try:
            logger.debug(f"Performing vector search for agent {agent_id}")
            # Note: This requires pgvector extension and proper setup
            # The actual implementation depends on Supabase's vector search capabilities
            query = await self.supabase.table(self.table_name).select("*").eq("agent_id", str(agent_id)).execute()
            
            # Vector search would typically use a custom RPC function
            # For now, we'll return a basic query structure
            # In production, you'd call an RPC function like:
            # result = await self.supabase.rpc('search_agent_memory', {
            #     'agent_id': str(agent_id),
            #     'query_embedding': embedding_vector,
            #     'match_threshold': similarity_threshold or 0.5,
            #     'match_count': limit
            # }).execute()
            
            logger.warning("Vector search not fully implemented. Requires RPC function setup.")
            return []
        except Exception as e:
            logger.error(f"Error performing vector search: {str(e)}")
            raise

