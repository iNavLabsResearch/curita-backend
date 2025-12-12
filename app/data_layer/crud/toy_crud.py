"""
CRUD operations for Toy entities.
Provides database operations for managing toys in the system.
"""
from typing import Optional, List
from uuid import UUID
from app.data_layer.crud.base_crud import BaseCRUD
from app.data_layer.data_classes.toy_schemas import (
    ToyCreate,
    ToyUpdate,
    ToyResponse
)
from app.data_layer.supabase_client import SupabaseClient
from app.telemetries.logger import logger


class ToyCRUD(BaseCRUD[ToyCreate, ToyUpdate, ToyResponse]):
    """
    CRUD operations for Toy entities.
    
    Handles all database operations related to toys including:
    - Basic CRUD operations (inherited from BaseCRUD)
    - Specialized queries for active toys
    - Name-based searches
    """
    
    def __init__(self, supabase_client: Optional[SupabaseClient] = None):
        """
        Initialize ToyCRUD instance.
        
        Args:
            supabase_client: Optional Supabase client instance
        """
        super().__init__(
            table_name="toys",
            response_model=ToyResponse,
            supabase_client=supabase_client
        )
    
    async def get_active_toys(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[ToyResponse]:
        """
        Retrieve all active toys.
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of active toy records
        """
        try:
            logger.debug(f"Fetching active toys with limit={limit}, offset={offset}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"is_active": True},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching active toys: {str(e)}", exc_info=True)
            return []
    
    async def get_by_name(self, name: str) -> Optional[ToyResponse]:
        """
        Retrieve a toy by its name.
        
        Args:
            name: Name of the toy to search for
            
        Returns:
            Toy record if found, None otherwise
        """
        try:
            logger.debug(f"Fetching toy by name: {name}")
            
            result = await self.supabase.select(
                self.table_name,
                filters={"name": name},
                limit=1
            )
            
            if result and len(result) > 0:
                logger.info(f"Successfully retrieved toy with name: {name}")
                return self.response_model(**result[0])
            
            logger.warning(f"Toy not found with name: {name}")
            return None
            
        except Exception as e:
            logger.error(f"Error fetching toy by name {name}: {str(e)}", exc_info=True)
            return None
    
    async def search_by_name(
        self,
        search_term: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[ToyResponse]:
        """
        Search toys by name pattern.
        
        Note: This is a simple implementation. For better search,
        consider using PostgreSQL full-text search or implementing
        a search service.
        
        Args:
            search_term: Search term to match against toy names
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of matching toy records
        """
        try:
            logger.debug(f"Searching toys with term: {search_term}")
            
            # Get all toys and filter in Python (basic implementation)
            # For production, use PostgreSQL LIKE or full-text search
            all_toys = await self.get_all(limit=1000, offset=0)
            
            matching_toys = [
                toy for toy in all_toys
                if search_term.lower() in toy.name.lower()
            ]
            
            # Apply pagination
            paginated_results = matching_toys[offset:offset + limit]
            
            logger.info(f"Found {len(matching_toys)} toys matching '{search_term}'")
            return paginated_results
            
        except Exception as e:
            logger.error(f"Error searching toys with term {search_term}: {str(e)}", exc_info=True)
            return []
    
    async def deactivate(self, id: UUID) -> Optional[ToyResponse]:
        """
        Deactivate a toy by setting is_active to False.
        
        Args:
            id: UUID of the toy to deactivate
            
        Returns:
            Updated toy record if successful, None otherwise
        """
        try:
            logger.debug(f"Deactivating toy with id: {id}")
            
            update_data = ToyUpdate(is_active=False)
            result = await self.update(id, update_data)
            
            if result:
                logger.info(f"Successfully deactivated toy with id: {id}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error deactivating toy with id {id}: {str(e)}", exc_info=True)
            return None
    
    async def activate(self, id: UUID) -> Optional[ToyResponse]:
        """
        Activate a toy by setting is_active to True.
        
        Args:
            id: UUID of the toy to activate
            
        Returns:
            Updated toy record if successful, None otherwise
        """
        try:
            logger.debug(f"Activating toy with id: {id}")
            
            update_data = ToyUpdate(is_active=True)
            result = await self.update(id, update_data)
            
            if result:
                logger.info(f"Successfully activated toy with id: {id}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error activating toy with id {id}: {str(e)}", exc_info=True)
            return None


# Singleton instance for easy access
_toy_crud_instance: Optional[ToyCRUD] = None


def get_toy_crud() -> ToyCRUD:
    """
    Get or create the singleton ToyCRUD instance.
    
    Returns:
        ToyCRUD instance
    """
    global _toy_crud_instance
    if _toy_crud_instance is None:
        _toy_crud_instance = ToyCRUD()
    return _toy_crud_instance
