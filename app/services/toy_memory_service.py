"""
Toy memory service for managing toy memory vectors
"""
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

from app.utilities.supabase_client import get_supabase
from app.services.base import BaseService
from app.services.embedding_service import get_embedding_service


class ToyMemoryService(BaseService):
    """Service for managing toy memory (interaction context)"""
    
    def __init__(self):
        """Initialize toy memory service"""
        super().__init__()
        self.table_name = self.settings.TOY_MEMORY_TABLE
        self.supabase = None
        self.embedding_service = None
        self.initialize()
    
    def initialize(self):
        """Initialize service resources"""
        self.logger.info(f"Initializing toy memory service for table: {self.table_name}")
        self.supabase = get_supabase()
        self.embedding_service = get_embedding_service()
        self.logger.info("Toy memory service initialized successfully")
    
    async def store_chunks(
        self,
        toy_id: UUID,
        chunks: List[Dict[str, Any]],
        content_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Store memory chunks with embeddings
        
        Args:
            toy_id: Toy UUID
            chunks: List of text chunks
            content_type: Type of content
            
        Returns:
            List of stored records
        """
        self.logger.info(f"Storing {len(chunks)} chunks to toy memory: {toy_id}")
        
        # Generate embeddings for all chunks
        chunk_texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedding_service.generate_embeddings(chunk_texts)
        
        records = []
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            record = {
                "toy_id": str(toy_id),
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
        
        self.logger.info(f"Successfully stored {len(response.data)} chunks to toy memory")
        return response.data
    
    def get_by_toy(self, toy_id: UUID, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get memory chunks for a toy
        
        Args:
            toy_id: Toy UUID
            limit: Maximum number of records
            
        Returns:
            List of memory chunks
        """
        self.logger.info(f"Fetching toy memory chunks: {toy_id}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("toy_id", str(toy_id))\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        
        self.logger.debug(f"Retrieved {len(response.data)} chunks for toy {toy_id}")
        return response.data
    
    def delete_by_toy(self, toy_id: UUID) -> bool:
        """
        Delete all memory for a toy
        
        Args:
            toy_id: Toy UUID
            
        Returns:
            True if deleted, False otherwise
        """
        self.logger.info(f"Deleting toy memory: {toy_id}")
        
        response = self.supabase.table(self.table_name)\
            .delete()\
            .eq("toy_id", str(toy_id))\
            .execute()
        
        self.logger.info(f"Toy memory deleted: {toy_id}")
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
        toy_id: Optional[UUID] = None,
        top_k: int = 5,
        similarity_threshold: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Semantic search in toy memory
        
        Args:
            query: Search query
            toy_id: Optional toy filter
            top_k: Number of results
            similarity_threshold: Minimum similarity score
            
        Returns:
            List of matching memory chunks
        """
        self.logger.info(f"Searching toy memory: query='{query[:50]}...', toy_id={toy_id}, top_k={top_k}")
        
        # Generate query embedding
        query_embedding = self.embedding_service.generate_embedding(query)
        
        # Call RPC function for vector search
        rpc_params = {
            "query_embedding": query_embedding,
            "match_count": top_k,
            "similarity_threshold": similarity_threshold
        }
        
        if toy_id:
            rpc_params["filter_toy_id"] = str(toy_id)
        
        response = self.supabase.rpc("match_toy_memory", rpc_params).execute()
        
        self.logger.info(f"Found {len(response.data)} matching memory chunks")
        return response.data


def get_toy_memory_service() -> ToyMemoryService:
    """Get toy memory service instance"""
    return ToyMemoryService()
