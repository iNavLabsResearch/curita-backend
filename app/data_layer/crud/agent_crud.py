"""
CRUD operations for Agent entities.
Provides database operations for managing agents in the system.
"""
from typing import Optional, List
from uuid import UUID
from app.data_layer.crud.base_crud import BaseCRUD
from app.data_layer.data_classes.agent_schemas import (
    AgentCreate,
    AgentUpdate,
    AgentResponse
)
from app.data_layer.supabase_client import SupabaseClient
from app.telemetries.logger import logger


class AgentCRUD(BaseCRUD[AgentCreate, AgentUpdate, AgentResponse]):
    """
    CRUD operations for Agent entities.
    
    Handles all database operations related to agents including:
    - Basic CRUD operations (inherited from BaseCRUD)
    - Queries by toy_id
    - Active agents filtering
    - Provider-specific queries
    """
    
    def __init__(self, supabase_client: Optional[SupabaseClient] = None):
        """
        Initialize AgentCRUD instance.
        
        Args:
            supabase_client: Optional Supabase client instance
        """
        super().__init__(
            table_name="agents",
            response_model=AgentResponse,
            supabase_client=supabase_client
        )
    
    async def get_by_toy_id(
        self,
        toy_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[AgentResponse]:
        """
        Retrieve all agents for a specific toy.
        
        Args:
            toy_id: UUID of the toy
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of agent records for the toy
        """
        try:
            logger.debug(f"Fetching agents for toy_id: {toy_id}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"toy_id": str(toy_id)},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching agents for toy_id {toy_id}: {str(e)}", exc_info=True)
            return []
    
    async def get_active_agents(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[AgentResponse]:
        """
        Retrieve all active agents across all toys.
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of active agent records
        """
        try:
            logger.debug(f"Fetching active agents with limit={limit}, offset={offset}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"is_active": True},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching active agents: {str(e)}", exc_info=True)
            return []
    
    async def get_active_by_toy_id(
        self,
        toy_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[AgentResponse]:
        """
        Retrieve all active agents for a specific toy.
        
        Args:
            toy_id: UUID of the toy
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of active agent records for the toy
        """
        try:
            logger.debug(f"Fetching active agents for toy_id: {toy_id}")
            
            # Note: Supabase select with multiple filters
            result = await self.supabase.select(
                self.table_name,
                filters={"toy_id": str(toy_id), "is_active": True},
                limit=limit,
                offset=offset,
                order_by="created_at",
                order_desc=True
            )
            
            if result:
                agents = [self.response_model(**record) for record in result]
                logger.info(f"Successfully retrieved {len(agents)} active agents for toy_id: {toy_id}")
                return agents
            
            logger.info(f"No active agents found for toy_id: {toy_id}")
            return []
            
        except Exception as e:
            logger.error(f"Error fetching active agents for toy_id {toy_id}: {str(e)}", exc_info=True)
            return []
    
    async def get_by_model_provider(
        self,
        model_provider_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[AgentResponse]:
        """
        Retrieve all agents using a specific model provider.
        
        Args:
            model_provider_id: UUID of the model provider
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of agent records using the provider
        """
        try:
            logger.debug(f"Fetching agents for model_provider_id: {model_provider_id}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"model_provider_id": str(model_provider_id)},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching agents for model_provider_id {model_provider_id}: {str(e)}", exc_info=True)
            return []
    
    async def get_by_tts_provider(
        self,
        tts_provider_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[AgentResponse]:
        """
        Retrieve all agents using a specific TTS provider.
        
        Args:
            tts_provider_id: UUID of the TTS provider
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of agent records using the provider
        """
        try:
            logger.debug(f"Fetching agents for tts_provider_id: {tts_provider_id}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"tts_provider_id": str(tts_provider_id)},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching agents for tts_provider_id {tts_provider_id}: {str(e)}", exc_info=True)
            return []
    
    async def get_by_transcriber_provider(
        self,
        transcriber_provider_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[AgentResponse]:
        """
        Retrieve all agents using a specific transcriber provider.
        
        Args:
            transcriber_provider_id: UUID of the transcriber provider
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of agent records using the provider
        """
        try:
            logger.debug(f"Fetching agents for transcriber_provider_id: {transcriber_provider_id}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"transcriber_provider_id": str(transcriber_provider_id)},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching agents for transcriber_provider_id {transcriber_provider_id}: {str(e)}", exc_info=True)
            return []
    
    async def get_by_language(
        self,
        language_code: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[AgentResponse]:
        """
        Retrieve all agents for a specific language.
        
        Args:
            language_code: Language code (e.g., 'en-US')
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of agent records for the language
        """
        try:
            logger.debug(f"Fetching agents for language_code: {language_code}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"language_code": language_code},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching agents for language_code {language_code}: {str(e)}", exc_info=True)
            return []
    
    async def deactivate(self, id: UUID) -> Optional[AgentResponse]:
        """
        Deactivate an agent by setting is_active to False.
        
        Args:
            id: UUID of the agent to deactivate
            
        Returns:
            Updated agent record if successful, None otherwise
        """
        try:
            logger.debug(f"Deactivating agent with id: {id}")
            
            update_data = AgentUpdate(is_active=False)
            result = await self.update(id, update_data)
            
            if result:
                logger.info(f"Successfully deactivated agent with id: {id}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error deactivating agent with id {id}: {str(e)}", exc_info=True)
            return None
    
    async def activate(self, id: UUID) -> Optional[AgentResponse]:
        """
        Activate an agent by setting is_active to True.
        
        Args:
            id: UUID of the agent to activate
            
        Returns:
            Updated agent record if successful, None otherwise
        """
        try:
            logger.debug(f"Activating agent with id: {id}")
            
            update_data = AgentUpdate(is_active=True)
            result = await self.update(id, update_data)
            
            if result:
                logger.info(f"Successfully activated agent with id: {id}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error activating agent with id {id}: {str(e)}", exc_info=True)
            return None


# Singleton instance for easy access
_agent_crud_instance: Optional[AgentCRUD] = None


def get_agent_crud() -> AgentCRUD:
    """
    Get or create the singleton AgentCRUD instance.
    
    Returns:
        AgentCRUD instance
    """
    global _agent_crud_instance
    if _agent_crud_instance is None:
        _agent_crud_instance = AgentCRUD()
    return _agent_crud_instance
