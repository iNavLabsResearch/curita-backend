"""
CRUD operations for Agent Tools
"""
from uuid import UUID
from typing import List
from app.data_layer.supabase_client import SupabaseClient
from app.data_layer.crud.base_crud import BaseCrud
from app.data_layer.data_classes.agent_schemas import AgentToolResponse
from app.telemetries.logger import logger


class AgentToolCRUD(BaseCrud):
    """CRUD operations for agent_tools table"""
    
    def __init__(self, supabase: SupabaseClient):
        super().__init__(supabase, "agent_tools", AgentToolResponse)
    
    async def get_tools_by_toy(self, toy_id: UUID) -> List[AgentToolResponse]:
        """
        Get all tools for a specific toy
        
        Args:
            toy_id: UUID of the toy
            
        Returns:
            List of agent tool records
        """
        try:
            logger.debug(f"Fetching tools for toy {toy_id}")
            return await self.filter_by(toy_id=str(toy_id))
        except Exception as e:
            logger.error(f"Error fetching tools for toy {toy_id}: {str(e)}")
            raise
    
    async def get_tools_by_name(self, name: str) -> List[AgentToolResponse]:
        """
        Get tools by name
        
        Args:
            name: Name of the tool
            
        Returns:
            List of agent tool records
        """
        try:
            logger.debug(f"Fetching tools by name: {name}")
            return await self.filter_by(name=name)
        except Exception as e:
            logger.error(f"Error fetching tools by name: {str(e)}")
            raise
    
    async def get_tools_by_provider(self, provider_name: str) -> List[AgentToolResponse]:
        """
        Get tools by provider name
        
        Args:
            provider_name: Name of the provider
            
        Returns:
            List of agent tool records
        """
        try:
            logger.debug(f"Fetching tools by provider: {provider_name}")
            return await self.filter_by(provider_name=provider_name)
        except Exception as e:
            logger.error(f"Error fetching tools by provider: {str(e)}")
            raise

