"""
CRUD operations for Agents
"""
from uuid import UUID
from typing import List, Dict, Any, Optional
from supabase import Client

from app.data_layer.crud.base_crud import BaseCrud
from app.telemetries.logger import logger


class AgentCRUD(BaseCrud):
    """CRUD operations for agents table"""
    
    def __init__(self, supabase_client: Client):
        super().__init__(supabase_client, "agents")
    
    async def get_agents_by_toy(self, toy_id: UUID) -> List[Dict[str, Any]]:
        """
        Get all agents for a specific toy
        
        Args:
            toy_id: UUID of the toy
            
        Returns:
            List of agent records
        """
        try:
            logger.debug(f"Fetching agents for toy {toy_id}")
            result = self.supabase.table(self.table_name).select("*").eq("toy_id", str(toy_id)).execute()
            return result.data
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
            result = self.supabase.table(self.table_name).select(
                "*, "
                "model_providers(*), "
                "tts_providers(*), "
                "transcriber_providers(*)"
            ).eq("id", str(agent_id)).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error fetching agent with providers: {str(e)}")
            raise
