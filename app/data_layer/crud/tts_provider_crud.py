"""
CRUD operations for TTS Provider entities.
Provides database operations for managing Text-to-Speech providers in the system.
"""
from typing import Optional, List
from uuid import UUID
from app.data_layer.crud.base_crud import BaseCRUD
from app.data_layer.data_classes.provider_schemas import (
    TTSProviderCreate,
    TTSProviderUpdate,
    TTSProviderResponse
)
from app.data_layer.supabase_client import SupabaseClient
from app.telemetries.logger import logger


class TTSProviderCRUD(BaseCRUD[TTSProviderCreate, TTSProviderUpdate, TTSProviderResponse]):
    """
    CRUD operations for TTS Provider entities.
    
    Handles all database operations related to TTS providers including:
    - Basic CRUD operations (inherited from BaseCRUD)
    - Default provider queries
    - Language-specific queries
    """
    
    def __init__(self, supabase_client: Optional[SupabaseClient] = None):
        """
        Initialize TTSProviderCRUD instance.
        
        Args:
            supabase_client: Optional Supabase client instance
        """
        super().__init__(
            table_name="tts_providers",
            response_model=TTSProviderResponse,
            supabase_client=supabase_client
        )
    
    async def get_default(self) -> Optional[TTSProviderResponse]:
        """
        Retrieve the default TTS provider.
        
        Returns:
            Default TTS provider record if found, None otherwise
        """
        try:
            logger.debug("Fetching default TTS provider")
            
            result = await self.supabase.select(
                self.table_name,
                filters={"is_default": True},
                limit=1,
                order_by="created_at",
                order_desc=False
            )
            
            if result and len(result) > 0:
                logger.info("Successfully retrieved default TTS provider")
                return self.response_model(**result[0])
            
            logger.warning("No default TTS provider found")
            return None
            
        except Exception as e:
            logger.error(f"Error fetching default TTS provider: {str(e)}", exc_info=True)
            return None
    
    async def get_by_provider_name(
        self,
        provider_name: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[TTSProviderResponse]:
        """
        Retrieve all TTS providers by provider name.
        
        Args:
            provider_name: Name of the provider
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of TTS provider records
        """
        try:
            logger.debug(f"Fetching TTS providers for provider_name: {provider_name}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"provider_name": provider_name},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching TTS providers for provider_name {provider_name}: {str(e)}", exc_info=True)
            return []
    
    async def set_default(self, id: UUID) -> Optional[TTSProviderResponse]:
        """
        Set a TTS provider as the default.
        This will unset any existing default provider.
        
        Args:
            id: UUID of the provider to set as default
            
        Returns:
            Updated provider record if successful, None otherwise
        """
        try:
            logger.debug(f"Setting TTS provider {id} as default")
            
            # First, unset all existing defaults
            all_providers = await self.get_all(filters={"is_default": True}, limit=1000)
            for provider in all_providers:
                await self.update(provider.id, TTSProviderUpdate(is_default=False))
            
            # Set the new default
            update_data = TTSProviderUpdate(is_default=True)
            result = await self.update(id, update_data)
            
            if result:
                logger.info(f"Successfully set TTS provider {id} as default")
            
            return result
            
        except Exception as e:
            logger.error(f"Error setting default TTS provider {id}: {str(e)}", exc_info=True)
            return None


# Singleton instance for easy access
_tts_provider_crud_instance: Optional[TTSProviderCRUD] = None


def get_tts_provider_crud() -> TTSProviderCRUD:
    """
    Get or create the singleton TTSProviderCRUD instance.
    
    Returns:
        TTSProviderCRUD instance
    """
    global _tts_provider_crud_instance
    if _tts_provider_crud_instance is None:
        _tts_provider_crud_instance = TTSProviderCRUD()
    return _tts_provider_crud_instance
