"""
CRUD operations for Agent Tool entities.
Provides database operations for managing agent tools in the system.
"""
from typing import Optional, List
from uuid import UUID
from app.data_layer.crud.base_crud import BaseCRUD
from app.data_layer.data_classes.agent_schemas import (
    AgentToolCreate,
    AgentToolUpdate,
    AgentToolResponse
)
from app.data_layer.supabase_client import SupabaseClient
from app.telemetries.logger import logger


class AgentToolCRUD(BaseCRUD[AgentToolCreate, AgentToolUpdate, AgentToolResponse]):
    """
    CRUD operations for Agent Tool entities.
    
    Handles all database operations related to agent tools including:
    - Basic CRUD operations (inherited from BaseCRUD)
    - Queries by toy_id
    - Queries by provider_name
    - HTTP method filtering
    """
    
    def __init__(self, supabase_client: Optional[SupabaseClient] = None):
        """
        Initialize AgentToolCRUD instance.
        
        Args:
            supabase_client: Optional Supabase client instance
        """
        super().__init__(
            table_name="agent_tools",
            response_model=AgentToolResponse,
            supabase_client=supabase_client
        )
    
    async def get_by_toy_id(
        self,
        toy_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[AgentToolResponse]:
        """
        Retrieve all tools for a specific toy.
        
        Args:
            toy_id: UUID of the toy
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of agent tool records for the toy
        """
        try:
            logger.debug(f"Fetching agent tools for toy_id: {toy_id}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"toy_id": str(toy_id)},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching agent tools for toy_id {toy_id}: {str(e)}", exc_info=True)
            return []
    
    async def get_by_provider_name(
        self,
        provider_name: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[AgentToolResponse]:
        """
        Retrieve all tools for a specific provider.
        
        Args:
            provider_name: Name of the tool provider
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of agent tool records for the provider
        """
        try:
            logger.debug(f"Fetching agent tools for provider_name: {provider_name}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"provider_name": provider_name},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching agent tools for provider_name {provider_name}: {str(e)}", exc_info=True)
            return []
    
    async def get_by_http_method(
        self,
        http_method: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[AgentToolResponse]:
        """
        Retrieve all tools using a specific HTTP method.
        
        Args:
            http_method: HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE')
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of agent tool records using the HTTP method
        """
        try:
            logger.debug(f"Fetching agent tools for http_method: {http_method}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"http_method": http_method.upper()},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching agent tools for http_method {http_method}: {str(e)}", exc_info=True)
            return []
    
    async def get_by_name(self, name: str) -> Optional[AgentToolResponse]:
        """
        Retrieve a tool by its name.
        
        Args:
            name: Name of the tool to search for
            
        Returns:
            Agent tool record if found, None otherwise
        """
        try:
            logger.debug(f"Fetching agent tool by name: {name}")
            
            result = await self.supabase.select(
                self.table_name,
                filters={"name": name},
                limit=1
            )
            
            if result and len(result) > 0:
                logger.info(f"Successfully retrieved agent tool with name: {name}")
                return self.response_model(**result[0])
            
            logger.warning(f"Agent tool not found with name: {name}")
            return None
            
        except Exception as e:
            logger.error(f"Error fetching agent tool by name {name}: {str(e)}", exc_info=True)
            return None
    
    async def search_by_name(
        self,
        search_term: str,
        toy_id: Optional[UUID] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[AgentToolResponse]:
        """
        Search tools by name pattern, optionally filtered by toy_id.
        
        Args:
            search_term: Search term to match against tool names
            toy_id: Optional UUID of the toy to filter by
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of matching agent tool records
        """
        try:
            logger.debug(f"Searching agent tools with term: {search_term}")
            
            # Get tools, filtered by toy_id if provided
            if toy_id:
                all_tools = await self.get_by_toy_id(toy_id, limit=1000, offset=0)
            else:
                all_tools = await self.get_all(limit=1000, offset=0)
            
            # Filter by search term
            matching_tools = [
                tool for tool in all_tools
                if search_term.lower() in tool.name.lower()
            ]
            
            # Apply pagination
            paginated_results = matching_tools[offset:offset + limit]
            
            logger.info(f"Found {len(matching_tools)} tools matching '{search_term}'")
            return paginated_results
            
        except Exception as e:
            logger.error(f"Error searching agent tools with term {search_term}: {str(e)}", exc_info=True)
            return []


# Singleton instance for easy access
_agent_tool_crud_instance: Optional[AgentToolCRUD] = None


def get_agent_tool_crud() -> AgentToolCRUD:
    """
    Get or create the singleton AgentToolCRUD instance.
    
    Returns:
        AgentToolCRUD instance
    """
    global _agent_tool_crud_instance
    if _agent_tool_crud_instance is None:
        _agent_tool_crud_instance = AgentToolCRUD()
    return _agent_tool_crud_instance
