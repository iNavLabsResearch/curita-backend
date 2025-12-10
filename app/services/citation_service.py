"""
Citation service for managing message citations
"""
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

from app.utilities.supabase_client import get_supabase
from app.services.base import BaseService


class CitationService(BaseService):
    """Service for managing message citations linking logs to memory"""
    
    def __init__(self):
        """Initialize citation service"""
        super().__init__()
        self.table_name = self.settings.MESSAGE_CITATIONS_TABLE
        self.supabase = None
        self.initialize()
    
    def initialize(self):
        """Initialize service resources"""
        self.logger.info(f"Initializing citation service for table: {self.table_name}")
        self.supabase = get_supabase()
        self.logger.info("Citation service initialized successfully")
    
    def add_citation(
        self,
        log_id: UUID,
        toy_memory_id: Optional[UUID] = None,
        agent_memory_id: Optional[UUID] = None,
        similarity_score: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Add a citation linking a message to memory
        
        Args:
            log_id: Conversation log UUID
            toy_memory_id: Toy memory UUID
            agent_memory_id: Agent memory UUID
            similarity_score: Similarity score
            
        Returns:
            Created citation record
        """
        if not toy_memory_id and not agent_memory_id:
            raise ValueError("Either toy_memory_id or agent_memory_id must be provided")
        
        self.logger.info(f"Adding citation: log={log_id}, toy_mem={toy_memory_id}, agent_mem={agent_memory_id}")
        
        citation_data = {
            "log_id": str(log_id),
            "toy_memory_id": str(toy_memory_id) if toy_memory_id else None,
            "agent_memory_id": str(agent_memory_id) if agent_memory_id else None,
            "similarity_score": similarity_score,
            "created_at": datetime.utcnow().isoformat()
        }
        
        response = self.supabase.table(self.table_name).insert(citation_data).execute()
        
        self.logger.info(f"Citation added: {response.data[0]['id']}")
        return response.data[0]
    
    def add_citations_batch(
        self,
        log_id: UUID,
        citations: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Add multiple citations for a message
        
        Args:
            log_id: Conversation log UUID
            citations: List of citation data
            
        Returns:
            List of created citation records
        """
        self.logger.info(f"Adding {len(citations)} citations for log: {log_id}")
        
        citation_records = []
        for citation in citations:
            record = {
                "log_id": str(log_id),
                "toy_memory_id": str(citation.get("toy_memory_id")) if citation.get("toy_memory_id") else None,
                "agent_memory_id": str(citation.get("agent_memory_id")) if citation.get("agent_memory_id") else None,
                "similarity_score": citation.get("similarity_score"),
                "created_at": datetime.utcnow().isoformat()
            }
            citation_records.append(record)
        
        response = self.supabase.table(self.table_name).insert(citation_records).execute()
        
        self.logger.info(f"Added {len(response.data)} citations")
        return response.data
    
    def get_by_log(self, log_id: UUID) -> List[Dict[str, Any]]:
        """
        Get all citations for a conversation log
        
        Args:
            log_id: Conversation log UUID
            
        Returns:
            List of citation records
        """
        self.logger.info(f"Fetching citations for log: {log_id}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("log_id", str(log_id))\
            .order("similarity_score", desc=True)\
            .execute()
        
        self.logger.debug(f"Retrieved {len(response.data)} citations for log {log_id}")
        return response.data
    
    def get_with_memory(self, log_id: UUID) -> List[Dict[str, Any]]:
        """
        Get citations with memory details
        
        Args:
            log_id: Conversation log UUID
            
        Returns:
            List of citations with memory data
        """
        self.logger.info(f"Fetching citations with memory for log: {log_id}")
        
        response = self.supabase.table(self.table_name)\
            .select("*, toy_memory(*), agent_memory(*)")\
            .eq("log_id", str(log_id))\
            .order("similarity_score", desc=True)\
            .execute()
        
        self.logger.debug(f"Retrieved {len(response.data)} citations with memory")
        return response.data
    
    def get_by_toy_memory(self, toy_memory_id: UUID) -> List[Dict[str, Any]]:
        """
        Get all citations referencing a toy memory chunk
        
        Args:
            toy_memory_id: Toy memory UUID
            
        Returns:
            List of citation records
        """
        self.logger.info(f"Fetching citations for toy memory: {toy_memory_id}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("toy_memory_id", str(toy_memory_id))\
            .execute()
        
        self.logger.debug(f"Retrieved {len(response.data)} citations")
        return response.data
    
    def get_by_agent_memory(self, agent_memory_id: UUID) -> List[Dict[str, Any]]:
        """
        Get all citations referencing an agent memory chunk
        
        Args:
            agent_memory_id: Agent memory UUID
            
        Returns:
            List of citation records
        """
        self.logger.info(f"Fetching citations for agent memory: {agent_memory_id}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("agent_memory_id", str(agent_memory_id))\
            .execute()
        
        self.logger.debug(f"Retrieved {len(response.data)} citations")
        return response.data
    
    def delete_by_log(self, log_id: UUID) -> bool:
        """
        Delete all citations for a conversation log
        
        Args:
            log_id: Conversation log UUID
            
        Returns:
            True if deleted
        """
        self.logger.info(f"Deleting citations for log: {log_id}")
        
        response = self.supabase.table(self.table_name)\
            .delete()\
            .eq("log_id", str(log_id))\
            .execute()
        
        self.logger.info(f"Citations deleted for log: {log_id}")
        return True
    
    def delete_by_id(self, citation_id: UUID) -> bool:
        """
        Delete a specific citation
        
        Args:
            citation_id: Citation UUID
            
        Returns:
            True if deleted, False otherwise
        """
        self.logger.info(f"Deleting citation: {citation_id}")
        
        response = self.supabase.table(self.table_name)\
            .delete()\
            .eq("id", str(citation_id))\
            .execute()
        
        success = len(response.data) > 0
        if success:
            self.logger.info(f"Citation deleted: {citation_id}")
        else:
            self.logger.warning(f"Citation not found: {citation_id}")
        
        return success


def get_citation_service() -> CitationService:
    """Get citation service instance"""
    return CitationService()
