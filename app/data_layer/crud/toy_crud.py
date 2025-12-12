"""
CRUD operations for Toys
"""
from uuid import UUID
from typing import List, Dict, Any, Optional
from app.data_layer.supabase_client import SupabaseClient
from app.data_layer.crud.base_crud import BaseCrud
from app.data_layer.data_classes.toy_schemas import ToyResponse
from app.telemetries.logger import logger


class ToyCRUD(BaseCrud):
    """CRUD operations for toys table"""
    
    def __init__(self, supabase: SupabaseClient):
        super().__init__(supabase, "toys", ToyResponse)
    
    async def get_active_toys(self) -> List[ToyResponse]:
        """
        Get all active toys
        
        Returns:
            List of active toy records
        """
        try:
            logger.debug("Fetching active toys")
            return await self.filter_by(is_active=True)
        except Exception as e:
            logger.error(f"Error fetching active toys: {str(e)}")
            raise
    
    async def get_toy_with_agents(self, toy_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get toy with all its agents
        
        Args:
            toy_id: UUID of the toy
            
        Returns:
            Toy record with agents array
        """
        try:
            logger.debug(f"Fetching toy {toy_id} with agents")
            result = await self.supabase.table(self.table_name).select(
                "*, agents(*)"
            ).eq("id", str(toy_id)).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error fetching toy with agents: {str(e)}")
            raise
