"""
Search service using Supabase RPC functions for vector similarity search
"""
from typing import List, Dict, Any, Optional
from app.utilities.supabase_client import get_supabase
from app.services.embedding_service import get_embedding_service
from app.services.base import BaseSearchService


class SupabaseSearchService(BaseSearchService):
    """Service for semantic search using Supabase pgvector RPC functions"""
    
    def __init__(self, table_name: str = None):
        """
        Initialize search service
        
        Args:
            table_name: Name of the table in Supabase
        """
        super().__init__()
        self.table_name = table_name or self.settings.DOCUMENTS_TABLE
        self.supabase = None
        self.embedding_service = None
        self.initialize()
    
    def initialize(self):
        """Initialize service resources"""
        self.logger.info("Initializing search service")
        self.supabase = get_supabase()
        self.embedding_service = get_embedding_service()
        self.logger.info("Search service initialized successfully")
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        similarity_threshold: Optional[float] = None,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search using RPC function
        
        Args:
            query: Search query text
            top_k: Number of results to return
            similarity_threshold: Minimum similarity score (0-1)
            filter_metadata: Optional metadata filters
            
        Returns:
            List of matching chunks with similarity scores
        """
        self.logger.info(f"Performing search: query='{query[:50]}...', top_k={top_k}")
        
        # Generate embedding for query
        query_embedding = self.embedding_service.generate_embedding(query)
        
        # Call Supabase RPC function for vector similarity search
        # The RPC function should be created in Supabase SQL editor
        rpc_params = {
            "query_embedding": query_embedding,
            "match_count": top_k
        }
        
        if similarity_threshold is not None:
            rpc_params["similarity_threshold"] = similarity_threshold
        
        if filter_metadata is not None:
            rpc_params["filter_metadata"] = filter_metadata
        
        response = self.supabase.rpc("match_documents", rpc_params).execute()
        
        self.logger.info(f"Search completed: found {len(response.data)} results")
        return response.data
    
    def search_by_document_id(
        self,
        query: str,
        document_id: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search within a specific document
        
        Args:
            query: Search query text
            document_id: Document to search within
            top_k: Number of results to return
            
        Returns:
            List of matching chunks from the specified document
        """
        self.logger.info(f"Searching in document: document_id={document_id}, query='{query[:50]}...', top_k={top_k}")
        query_embedding = self.embedding_service.generate_embedding(query)
        
        rpc_params = {
            "query_embedding": query_embedding,
            "match_count": top_k,
            "filter_document_id": document_id
        }
        
        response = self.supabase.rpc("match_documents_by_id", rpc_params).execute()
        
        self.logger.info(f"Document search completed: found {len(response.data)} results")
        return response.data
    
def get_search_service() -> SupabaseSearchService:
    """Get search service instance"""
    return SupabaseSearchService()
