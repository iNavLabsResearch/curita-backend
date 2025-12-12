"""
CRUD operations for Agents
"""
from uuid import UUID
from typing import List, Dict, Any, Optional
from app.data_layer.supabase_client import SupabaseClient
from app.data_layer.crud.base_crud import BaseCrud
from app.data_layer.data_classes.agent_schemas import AgentResponse
from app.telemetries.logger import logger


class AgentCRUD(BaseCrud):
    """CRUD operations for agents table"""
    
    def __init__(self, supabase: SupabaseClient):
        super().__init__(supabase, "agents", AgentResponse)
    
    async def get_agents_by_toy(self, toy_id: UUID) -> List[AgentResponse]:
        """
        Get all agents for a specific toy
        
        Args:
            toy_id: UUID of the toy
            
        Returns:
            List of agent records
        """
        try:
            logger.debug(f"Fetching agents for toy {toy_id}")
            return await self.filter_by(toy_id=str(toy_id))
        except Exception as e:
            logger.error(f"Error fetching agents for toy {toy_id}: {str(e)}")
            raise
    
    async def get_agent_with_providers(self, agent_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get agent with all provider details
        
        Args:
            agent_id: UUID of the agent
            
        Returns:
            Agent record with provider details
        """
        try:
            logger.debug(f"Fetching agent {agent_id} with providers")
            result = await self.supabase.table(self.table_name).select(
                "*, "
                "model_providers(*), "
                "tts_providers(*), "
                "transcriber_providers(*)"
            ).eq("id", str(agent_id)).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error fetching agent with providers: {str(e)}")
            raise
