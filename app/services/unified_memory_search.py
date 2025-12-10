"""
Unified memory search service for toy and agent memory
"""
from typing import List, Dict, Any, Optional
from uuid import UUID

from app.services.base import BaseService
from app.services.toy_memory_service import get_toy_memory_service
from app.services.agent_memory_service import get_agent_memory_service


class UnifiedMemorySearchService(BaseService):
    """Service for searching across toy and agent memory"""
    
    def __init__(self):
        """Initialize unified search service"""
        super().__init__()
        self.toy_memory_service = None
        self.agent_memory_service = None
        self.initialize()
    
    def initialize(self):
        """Initialize service resources"""
        self.logger.info("Initializing unified memory search service")
        self.toy_memory_service = get_toy_memory_service()
        self.agent_memory_service = get_agent_memory_service()
        self.logger.info("Unified memory search service initialized")
    
    def search(
        self,
        query: str,
        memory_type: str = "both",
        toy_id: Optional[UUID] = None,
        agent_id: Optional[UUID] = None,
        top_k: int = 5,
        similarity_threshold: float = 0.0
    ) -> Dict[str, Any]:
        """
        Search across toy memory, agent memory, or both
        
        Args:
            query: Search query
            memory_type: Type of memory to search ('toy', 'agent', 'both')
            toy_id: Optional toy filter
            agent_id: Optional agent filter
            top_k: Number of results per memory type
            similarity_threshold: Minimum similarity score
            
        Returns:
            Dictionary with search results by type
        """
        self.logger.info(f"Unified memory search: query='{query[:50]}...', type={memory_type}, toy={toy_id}, agent={agent_id}")
        
        results = {
            "toy_memory": [],
            "agent_memory": [],
            "combined": []
        }
        
        # Search toy memory
        if memory_type in ("toy", "both"):
            try:
                toy_results = self.toy_memory_service.search(
                    query=query,
                    toy_id=toy_id,
                    top_k=top_k,
                    similarity_threshold=similarity_threshold
                )
                # Add memory type to results
                for result in toy_results:
                    result["memory_type"] = "toy"
                results["toy_memory"] = toy_results
                self.logger.debug(f"Found {len(toy_results)} toy memory results")
            except Exception as e:
                self.logger.error(f"Error searching toy memory: {str(e)}")
        
        # Search agent memory
        if memory_type in ("agent", "both"):
            try:
                agent_results = self.agent_memory_service.search(
                    query=query,
                    agent_id=agent_id,
                    toy_id=toy_id,
                    top_k=top_k,
                    similarity_threshold=similarity_threshold
                )
                # Add memory type to results
                for result in agent_results:
                    result["memory_type"] = "agent"
                results["agent_memory"] = agent_results
                self.logger.debug(f"Found {len(agent_results)} agent memory results")
            except Exception as e:
                self.logger.error(f"Error searching agent memory: {str(e)}")
        
        # Combine and sort by similarity if searching both
        if memory_type == "both":
            combined = results["toy_memory"] + results["agent_memory"]
            combined.sort(key=lambda x: x.get("similarity", 0), reverse=True)
            results["combined"] = combined[:top_k]
            self.logger.info(f"Combined search returned {len(results['combined'])} results")
        else:
            # If single type, put results in combined too
            results["combined"] = results["toy_memory"] if memory_type == "toy" else results["agent_memory"]
        
        return results
    
    def search_with_context(
        self,
        query: str,
        agent_id: UUID,
        top_k_per_type: int = 3,
        similarity_threshold: float = 0.3
    ) -> Dict[str, Any]:
        """
        Search for context combining toy and agent memory for an agent
        
        Args:
            query: Search query
            agent_id: Agent UUID to get toy_id from
            top_k_per_type: Results per memory type
            similarity_threshold: Minimum similarity
            
        Returns:
            Contextual search results
        """
        self.logger.info(f"Context search for agent: {agent_id}, query='{query[:50]}...'")
        
        # Get agent to find toy_id
        from app.services.agent_service import get_agent_service
        agent_service = get_agent_service()
        agent = agent_service.get_by_id(agent_id)
        
        if not agent:
            self.logger.error(f"Agent not found: {agent_id}")
            return {"toy_memory": [], "agent_memory": [], "combined": []}
        
        toy_id = UUID(agent["toy_id"])
        
        # Search both memory types
        results = self.search(
            query=query,
            memory_type="both",
            toy_id=toy_id,
            agent_id=agent_id,
            top_k=top_k_per_type,
            similarity_threshold=similarity_threshold
        )
        
        self.logger.info(f"Context search returned {len(results['combined'])} total results")
        return results


def get_unified_memory_search_service() -> UnifiedMemorySearchService:
    """Get unified memory search service instance"""
    return UnifiedMemorySearchService()
