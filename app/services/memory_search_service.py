"""
Memory search service
Runs query -> local embedding -> Supabase RPC similarity search
"""
from typing import Dict, Any, List, Optional
from uuid import UUID

from app.services.base import BaseDatabaseService
from app.services.embedding_service import get_embedding_service


class MemorySearchService(BaseDatabaseService):
    """Service for searching toy/agent memory via Supabase RPC functions."""

    def __init__(self):
        super().__init__(table_name=None)
        self.embedding_service = None

    async def initialize(self):
        """Initialize Supabase and embedding service."""
        if self._initialized:
            return

        await super().initialize()
        self.embedding_service = get_embedding_service()
        self._initialized = True
        self.logger.info("MemorySearchService initialized")

    async def search_memory(
        self,
        query_text: str,
        match_count: int = 5,
        similarity_threshold: float = 0.0,
        toy_id: Optional[UUID] = None,
        agent_id: Optional[UUID] = None,
        scope: str = "all",
    ) -> List[Dict[str, Any]]:
        """
        Search memory using Supabase RPC functions.

        Args:
            query_text: User query to embed and search with.
            match_count: Max results to return.
            similarity_threshold: Minimum similarity (0-1).
            toy_id: Optional filter.
            agent_id: Optional filter (agent/all scopes).
            scope: "toy", "agent", or "all".
        """
        await self.initialize()

        if not query_text or not query_text.strip():
            self.logger.warning("Empty query_text provided to search_memory")
            return []

        rpc_name, params = self._build_rpc_payload(
            query_text=query_text,
            match_count=match_count,
            similarity_threshold=similarity_threshold,
            toy_id=toy_id,
            agent_id=agent_id,
            scope=scope,
        )

        if not rpc_name:
            self.logger.error(f"Invalid scope provided: {scope}")
            return []

        try:
            response = await self.supabase.call_rpc_function(rpc_name, params)
            return response or []
        except Exception as e:
            self.logger.error(f"RPC search failed for {rpc_name}: {str(e)}", exc_info=True)
            raise

    def _build_rpc_payload(
        self,
        query_text: str,
        match_count: int,
        similarity_threshold: float,
        toy_id: Optional[UUID],
        agent_id: Optional[UUID],
        scope: str,
    ) -> (Optional[str], Dict[str, Any]):
        """Prepare RPC name and parameters."""
        embedding = self.embedding_service.generate_embedding(query_text)

        base_params: Dict[str, Any] = {
            "query_embedding": embedding,
            "match_count": match_count,
            "similarity_threshold": similarity_threshold,
        }

        if scope == "toy":
            rpc_name = "match_toy_memory"
            base_params["filter_toy_id"] = str(toy_id) if toy_id else None
        elif scope == "agent":
            rpc_name = "match_agent_memory"
            base_params["filter_toy_id"] = str(toy_id) if toy_id else None
            base_params["filter_agent_id"] = str(agent_id) if agent_id else None
        elif scope == "all":
            rpc_name = "match_all_memory"
            base_params["filter_toy_id"] = str(toy_id) if toy_id else None
            base_params["filter_agent_id"] = str(agent_id) if agent_id else None
        else:
            rpc_name = None

        return rpc_name, base_params


def get_memory_search_service() -> MemorySearchService:
    """Factory for memory search service."""
    return MemorySearchService()

