"""
Provider services for managing model, TTS, and transcriber providers
"""
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

from app.data_layer.supabase_client import get_supabase
from app.services.base import BaseService


class ProviderService(BaseService):
    """Base service for provider management"""
    
    def __init__(self, table_name: str):
        """
        Initialize provider service
        
        Args:
            table_name: Name of the provider table
        """
        super().__init__()
        self.table_name = table_name
        self.supabase = None
        self.initialize()
    
    def initialize(self):
        """Initialize service resources"""
        self.logger.info(f"Initializing provider service for table: {self.table_name}")
        self.supabase = get_supabase()
        self.logger.info(f"Provider service initialized: {self.table_name}")
    
    def create(self, provider_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new provider
        
        Args:
            provider_data: Provider data
            
        Returns:
            Created provider record
        """
        self.logger.info(f"Creating provider in {self.table_name}: {provider_data.get('provider_name')}")
        
        # Add timestamps
        provider_data["created_at"] = datetime.utcnow().isoformat()
        provider_data["updated_at"] = datetime.utcnow().isoformat()
        
        response = self.supabase.table(self.table_name).insert(provider_data).execute()
        
        self.logger.info(f"Provider created successfully: {response.data[0]['id']}")
        return response.data[0]
    
    def get_by_id(self, provider_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get provider by ID
        
        Args:
            provider_id: Provider UUID
            
        Returns:
            Provider record or None
        """
        self.logger.info(f"Fetching provider: {provider_id}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("id", str(provider_id))\
            .execute()
        
        if response.data:
            return response.data[0]
        
        self.logger.warning(f"Provider not found: {provider_id}")
        return None
    
    def list(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        List all providers with pagination
        
        Args:
            limit: Maximum number of records
            offset: Number of records to skip
            
        Returns:
            List of provider records
        """
        self.logger.info(f"Listing providers from {self.table_name}: limit={limit}, offset={offset}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .order("created_at", desc=True)\
            .range(offset, offset + limit - 1)\
            .execute()
        
        self.logger.debug(f"Retrieved {len(response.data)} providers")
        return response.data
    
    def get_default(self) -> Optional[Dict[str, Any]]:
        """
        Get the default provider
        
        Returns:
            Default provider record or None
        """
        self.logger.info(f"Fetching default provider from {self.table_name}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("is_default", True)\
            .execute()
        
        if response.data:
            return response.data[0]
        
        self.logger.warning(f"No default provider found in {self.table_name}")
        return None
    
    def update(self, provider_id: UUID, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update provider
        
        Args:
            provider_id: Provider UUID
            updates: Fields to update
            
        Returns:
            Updated provider record or None
        """
        self.logger.info(f"Updating provider: {provider_id}")
        
        # Add updated timestamp
        updates["updated_at"] = datetime.utcnow().isoformat()
        
        response = self.supabase.table(self.table_name)\
            .update(updates)\
            .eq("id", str(provider_id))\
            .execute()
        
        if response.data:
            self.logger.info(f"Provider updated successfully: {provider_id}")
            return response.data[0]
        
        self.logger.warning(f"Provider not found for update: {provider_id}")
        return None
    
    def delete(self, provider_id: UUID) -> bool:
        """
        Delete provider
        
        Args:
            provider_id: Provider UUID
            
        Returns:
            True if deleted, False otherwise
        """
        self.logger.info(f"Deleting provider: {provider_id}")
        
        response = self.supabase.table(self.table_name)\
            .delete()\
            .eq("id", str(provider_id))\
            .execute()
        
        success = len(response.data) > 0
        if success:
            self.logger.info(f"Provider deleted successfully: {provider_id}")
        else:
            self.logger.warning(f"Provider not found for deletion: {provider_id}")
        
        return success
    
    def set_default(self, provider_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Set a provider as default (unsets all others)
        
        Args:
            provider_id: Provider UUID to set as default
            
        Returns:
            Updated provider record or None
        """
        self.logger.info(f"Setting provider as default: {provider_id}")
        
        # First, unset all defaults
        self.supabase.table(self.table_name)\
            .update({"is_default": False, "updated_at": datetime.utcnow().isoformat()})\
            .eq("is_default", True)\
            .execute()
        
        # Then set the new default
        response = self.supabase.table(self.table_name)\
            .update({"is_default": True, "updated_at": datetime.utcnow().isoformat()})\
            .eq("id", str(provider_id))\
            .execute()
        
        if response.data:
            self.logger.info(f"Provider set as default: {provider_id}")
            return response.data[0]
        
        self.logger.warning(f"Provider not found to set as default: {provider_id}")
        return None


class ModelProviderService(ProviderService):
    """Service for managing model providers"""
    
    def __init__(self):
        from static_memory_cache import StaticMemoryCache
        super().__init__("providers")


class TTSProviderService(ProviderService):
    """Service for managing TTS providers"""
    
    def __init__(self):
        from static_memory_cache import StaticMemoryCache
        super().__init__("providers")


class TranscriberProviderService(ProviderService):
    """Service for managing transcriber providers"""
    
    def __init__(self):
        from static_memory_cache import StaticMemoryCache
        super().__init__("providers")


# Service factory functions
def get_model_provider_service() -> ModelProviderService:
    """Get model provider service instance"""
    return ModelProviderService()


def get_tts_provider_service() -> TTSProviderService:
    """Get TTS provider service instance"""
    return TTSProviderService()


def get_transcriber_provider_service() -> TranscriberProviderService:
    """Get transcriber provider service instance"""
    return TranscriberProviderService()
