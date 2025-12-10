"""
Agent memory service for managing agent knowledge base
"""
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

from app.data_layer.supabase_client import get_supabase
from app.services.base import BaseService
from app.services.embedding_service import get_embedding_service


class AgentMemoryService(BaseService):
    """Service for managing agent memory (knowledge base with file storage)"""
    
    def __init__(self):
        """Initialize agent memory service"""
        super().__init__()
        self.table_name = self.settings.AGENT_MEMORY_TABLE
        self.supabase = None
        self.embedding_service = None
        self.initialize()
    
    def initialize(self):
        """Initialize service resources"""
        self.logger.info(f"Initializing agent memory service for table: {self.table_name}")
        self.supabase = get_supabase()
        self.embedding_service = get_embedding_service()
        self.logger.info("Agent memory service initialized successfully")
    
    async def store_chunks(
        self,
        toy_id: UUID,
        agent_id: UUID,
        chunks: List[Dict[str, Any]],
        original_filename: Optional[str] = None,
        storage_file_id: Optional[str] = None,
        file_size: Optional[int] = None,
        content_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Store agent memory chunks with embeddings
        
        Args:
            toy_id: Toy UUID
            agent_id: Agent UUID
            chunks: List of text chunks
            original_filename: Original file name
            storage_file_id: Storage file identifier
            file_size: File size in bytes
            content_type: Content type
            
        Returns:
            List of stored records
        """
        self.logger.info(f"Storing {len(chunks)} chunks to agent memory: agent={agent_id}, toy={toy_id}")
        
        # Generate embeddings for all chunks
        chunk_texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedding_service.generate_embeddings(chunk_texts)
        
        records = []
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            record = {
                "toy_id": str(toy_id),
                "agent_id": str(agent_id),
                "original_filename": original_filename,
                "storage_file_id": storage_file_id,
                "file_size": file_size,
                "content_type": content_type,
                "chunk_text": chunk["text"],
                "embedding_vector": embedding,
                "chunk_index": idx,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            records.append(record)
        
        # Insert into Supabase
        response = self.supabase.table(self.table_name).insert(records).execute()
        
        self.logger.info(f"Successfully stored {len(response.data)} chunks to agent memory")
        return response.data
    
    def get_by_agent(self, agent_id: UUID, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get memory chunks for an agent
        
        Args:
            agent_id: Agent UUID
            limit: Maximum number of records
            
        Returns:
            List of memory chunks
        """
        self.logger.info(f"Fetching agent memory chunks: {agent_id}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("agent_id", str(agent_id))\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        
        self.logger.debug(f"Retrieved {len(response.data)} chunks for agent {agent_id}")
        return response.data
    
    def get_by_toy(self, toy_id: UUID, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all agent memory for a toy
        
        Args:
            toy_id: Toy UUID
            limit: Maximum number of records
            
        Returns:
            List of memory chunks
        """
        self.logger.info(f"Fetching agent memory for toy: {toy_id}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("toy_id", str(toy_id))\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        
        self.logger.debug(f"Retrieved {len(response.data)} chunks for toy {toy_id}")
        return response.data
    
    def get_by_file(self, storage_file_id: str) -> List[Dict[str, Any]]:
        """
        Get memory chunks for a specific file
        
        Args:
            storage_file_id: Storage file identifier
            
        Returns:
            List of memory chunks
        """
        self.logger.info(f"Fetching agent memory for file: {storage_file_id}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("storage_file_id", storage_file_id)\
            .order("chunk_index")\
            .execute()
        
        self.logger.debug(f"Retrieved {len(response.data)} chunks for file {storage_file_id}")
        return response.data
    
    def delete_by_agent(self, agent_id: UUID) -> bool:
        """
        Delete all memory for an agent
        
        Args:
            agent_id: Agent UUID
            
        Returns:
            True if deleted
        """
        self.logger.info(f"Deleting agent memory: {agent_id}")
        
        response = self.supabase.table(self.table_name)\
            .delete()\
            .eq("agent_id", str(agent_id))\
            .execute()
        
        self.logger.info(f"Agent memory deleted: {agent_id}")
        return True
    
    def delete_by_file(self, storage_file_id: str) -> bool:
        """
        Delete all memory for a specific file
        
        Args:
            storage_file_id: Storage file identifier
            
        Returns:
            True if deleted
        """
        self.logger.info(f"Deleting agent memory for file: {storage_file_id}")
        
        response = self.supabase.table(self.table_name)\
            .delete()\
            .eq("storage_file_id", storage_file_id)\
            .execute()
        
        self.logger.info(f"Agent memory deleted for file: {storage_file_id}")
        return True
    
    def delete_by_id(self, memory_id: UUID) -> bool:
        """
        Delete a specific memory chunk
        
        Args:
            memory_id: Memory UUID
            
        Returns:
            True if deleted, False otherwise
        """
        self.logger.info(f"Deleting memory chunk: {memory_id}")
        
        response = self.supabase.table(self.table_name)\
            .delete()\
            .eq("id", str(memory_id))\
            .execute()
        
        success = len(response.data) > 0
        if success:
            self.logger.info(f"Memory chunk deleted: {memory_id}")
        else:
            self.logger.warning(f"Memory chunk not found: {memory_id}")
        
        return success
    
    def search(
        self,
        query: str,
        agent_id: Optional[UUID] = None,
        toy_id: Optional[UUID] = None,
        top_k: int = 5,
        similarity_threshold: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Semantic search in agent memory
        
        Args:
            query: Search query
            agent_id: Optional agent filter
            toy_id: Optional toy filter
            top_k: Number of results
            similarity_threshold: Minimum similarity score
            
        Returns:
            List of matching memory chunks
        """
        self.logger.info(f"Searching agent memory: query='{query[:50]}...', agent={agent_id}, toy={toy_id}, top_k={top_k}")
        
        # Generate query embedding
        query_embedding = self.embedding_service.generate_embedding(query)
        
        # Call RPC function for vector search
        rpc_params = {
            "query_embedding": query_embedding,
            "match_count": top_k,
            "similarity_threshold": similarity_threshold
        }
        
        if agent_id:
            rpc_params["filter_agent_id"] = str(agent_id)
        if toy_id:
            rpc_params["filter_toy_id"] = str(toy_id)
        
        response = self.supabase.rpc("match_agent_memory", rpc_params).execute()
        
        self.logger.info(f"Found {len(response.data)} matching memory chunks")
        return response.data


def get_agent_memory_service() -> AgentMemoryService:
    """Get agent memory service instance"""
    return AgentMemoryService()
