"""
CRUD operations for Toys
"""
from uuid import UUID
from typing import List, Dict, Any, Optional
from supabase import Client

from app.data_layer.crud.base_crud import BaseCrud
from app.telemetries.logger import logger


class ToyCRUD(BaseCrud):
    """CRUD operations for toys table"""
    
    def __init__(self, supabase_client: Client):
        super().__init__(supabase_client, "toys")
    
    async def get_active_toys(self) -> List[Dict[str, Any]]:
        """
        Get all active toys
        
        Returns:
            List of active toy records
        """
        try:
            logger.debug("Fetching active toys")
            result = self.supabase.table(self.table_name).select("*").eq("is_active", True).execute()
            return result.data
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
            result = self.supabase.table(self.table_name).select(
                "*, agents(*)"
            ).eq("id", str(toy_id)).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error fetching toy with agents: {str(e)}")
            raise
