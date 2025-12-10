"""
Toy service for managing toys
"""
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

from app.data_layer.supabase_client import get_supabase
from app.services.base import BaseService


class ToyService(BaseService):
    """Service for managing toys"""
    
    def __init__(self):
        """Initialize toy service"""
        super().__init__()
        self.table_name = self.settings.TOYS_TABLE
        self.supabase = None
        self.initialize()
    
    def initialize(self):
        """Initialize service resources"""
        self.logger.info(f"Initializing toy service for table: {self.table_name}")
        self.supabase = get_supabase()
        self.logger.info("Toy service initialized successfully")
    
    def create(self, toy_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new toy
        
        Args:
            toy_data: Toy data
            
        Returns:
            Created toy record
        """
        self.logger.info(f"Creating toy: {toy_data.get('name')}")
        
        # Add timestamps
        toy_data["created_at"] = datetime.utcnow().isoformat()
        toy_data["updated_at"] = datetime.utcnow().isoformat()
        
        response = self.supabase.table(self.table_name).insert(toy_data).execute()
        
        self.logger.info(f"Toy created successfully: {response.data[0]['id']}")
        return response.data[0]
    
    def get_by_id(self, toy_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get toy by ID
        
        Args:
            toy_id: Toy UUID
            
        Returns:
            Toy record or None
        """
        self.logger.info(f"Fetching toy: {toy_id}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("id", str(toy_id))\
            .execute()
        
        if response.data:
            return response.data[0]
        
        self.logger.warning(f"Toy not found: {toy_id}")
        return None
    
    def list(self, limit: int = 100, offset: int = 0, is_active: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        List toys with pagination
        
        Args:
            limit: Maximum number of records
            offset: Number of records to skip
            is_active: Filter by active status
            
        Returns:
            List of toy records
        """
        self.logger.info(f"Listing toys: limit={limit}, offset={offset}, is_active={is_active}")
        
        query = self.supabase.table(self.table_name).select("*")
        
        if is_active is not None:
            query = query.eq("is_active", is_active)
        
        response = query.order("created_at", desc=True)\
            .range(offset, offset + limit - 1)\
            .execute()
        
        self.logger.debug(f"Retrieved {len(response.data)} toys")
        return response.data
    
    def update(self, toy_id: UUID, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update toy
        
        Args:
            toy_id: Toy UUID
            updates: Fields to update
            
        Returns:
            Updated toy record or None
        """
        self.logger.info(f"Updating toy: {toy_id}")
        
        # Add updated timestamp
        updates["updated_at"] = datetime.utcnow().isoformat()
        
        response = self.supabase.table(self.table_name)\
            .update(updates)\
            .eq("id", str(toy_id))\
            .execute()
        
        if response.data:
            self.logger.info(f"Toy updated successfully: {toy_id}")
            return response.data[0]
        
        self.logger.warning(f"Toy not found for update: {toy_id}")
        return None
    
    def delete(self, toy_id: UUID) -> bool:
        """
        Delete toy (will cascade to agents, tools, memories)
        
        Args:
            toy_id: Toy UUID
            
        Returns:
            True if deleted, False otherwise
        """
        self.logger.info(f"Deleting toy: {toy_id}")
        
        response = self.supabase.table(self.table_name)\
            .delete()\
            .eq("id", str(toy_id))\
            .execute()
        
        success = len(response.data) > 0
        if success:
            self.logger.info(f"Toy deleted successfully: {toy_id}")
        else:
            self.logger.warning(f"Toy not found for deletion: {toy_id}")
        
        return success
    
    def activate(self, toy_id: UUID, is_active: bool = True) -> Optional[Dict[str, Any]]:
        """
        Activate or deactivate a toy
        
        Args:
            toy_id: Toy UUID
            is_active: Activation status
            
        Returns:
            Updated toy record or None
        """
        self.logger.info(f"{'Activating' if is_active else 'Deactivating'} toy: {toy_id}")
        
        return self.update(toy_id, {"is_active": is_active})
    
    def get_with_agents(self, toy_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get toy with its agents
        
        Args:
            toy_id: Toy UUID
            
        Returns:
            Toy record with agents or None
        """
        self.logger.info(f"Fetching toy with agents: {toy_id}")
        
        response = self.supabase.table(self.table_name)\
            .select("*, agents(*)")\
            .eq("id", str(toy_id))\
            .execute()
        
        if response.data:
            return response.data[0]
        
        self.logger.warning(f"Toy not found: {toy_id}")
        return None


def get_toy_service() -> ToyService:
    """Get toy service instance"""
    return ToyService()
