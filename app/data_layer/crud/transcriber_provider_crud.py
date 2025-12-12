"""
CRUD operations for Transcriber Provider entities.
Provides database operations for managing Speech-to-Text providers in the system.
"""
from typing import Optional, List
from uuid import UUID
from app.data_layer.crud.base_crud import BaseCRUD
from app.data_layer.data_classes.provider_schemas import (
    TranscriberProviderCreate,
    TranscriberProviderUpdate,
    TranscriberProviderResponse
)
from app.data_layer.supabase_client import SupabaseClient
from app.telemetries.logger import logger


class TranscriberProviderCRUD(BaseCRUD[TranscriberProviderCreate, TranscriberProviderUpdate, TranscriberProviderResponse]):
    """
    CRUD operations for Transcriber Provider entities.
    
    Handles all database operations related to transcriber providers including:
    - Basic CRUD operations (inherited from BaseCRUD)
    - Default provider queries
    - Language-specific queries
    - Model size filtering
    """
    
    def __init__(self, supabase_client: Optional[SupabaseClient] = None):
        """
        Initialize TranscriberProviderCRUD instance.
        
        Args:
            supabase_client: Optional Supabase client instance
        """
        super().__init__(
            table_name="transcriber_providers",
            response_model=TranscriberProviderResponse,
            supabase_client=supabase_client
        )
    
    async def get_default(self) -> Optional[TranscriberProviderResponse]:
        """
        Retrieve the default transcriber provider.
        
        Returns:
            Default transcriber provider record if found, None otherwise
        """
        try:
            logger.debug("Fetching default transcriber provider")
            
            result = await self.supabase.select(
                self.table_name,
                filters={"is_default": True},
                limit=1,
                order_by="created_at",
                order_desc=False
            )
            
            if result and len(result) > 0:
                logger.info("Successfully retrieved default transcriber provider")
                return self.response_model(**result[0])
            
            logger.warning("No default transcriber provider found")
            return None
            
        except Exception as e:
            logger.error(f"Error fetching default transcriber provider: {str(e)}", exc_info=True)
            return None
    
    async def get_by_provider_name(
        self,
        provider_name: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[TranscriberProviderResponse]:
        """
        Retrieve all transcriber providers by provider name.
        
        Args:
            provider_name: Name of the provider
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of transcriber provider records
        """
        try:
            logger.debug(f"Fetching transcriber providers for provider_name: {provider_name}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"provider_name": provider_name},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching transcriber providers for provider_name {provider_name}: {str(e)}", exc_info=True)
            return []
    
    async def get_by_model_size(
        self,
        model_size: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[TranscriberProviderResponse]:
        """
        Retrieve all transcriber providers by model size.
        
        Args:
            model_size: Model size (e.g., 'tiny', 'base', 'small', 'medium', 'large')
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of transcriber provider records
        """
        try:
            logger.debug(f"Fetching transcriber providers for model_size: {model_size}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"model_size": model_size},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching transcriber providers for model_size {model_size}: {str(e)}", exc_info=True)
            return []
    
    async def set_default(self, id: UUID) -> Optional[TranscriberProviderResponse]:
        """
        Set a transcriber provider as the default.
        This will unset any existing default provider.
        
        Args:
            id: UUID of the provider to set as default
            
        Returns:
            Updated provider record if successful, None otherwise
        """
        try:
            logger.debug(f"Setting transcriber provider {id} as default")
            
            # First, unset all existing defaults
            all_providers = await self.get_all(filters={"is_default": True}, limit=1000)
            for provider in all_providers:
                await self.update(provider.id, TranscriberProviderUpdate(is_default=False))
            
            # Set the new default
            update_data = TranscriberProviderUpdate(is_default=True)
            result = await self.update(id, update_data)
            
            if result:
                logger.info(f"Successfully set transcriber provider {id} as default")
            
            return result
            
        except Exception as e:
            logger.error(f"Error setting default transcriber provider {id}: {str(e)}", exc_info=True)
            return None


# Singleton instance for easy access
_transcriber_provider_crud_instance: Optional[TranscriberProviderCRUD] = None


def get_transcriber_provider_crud() -> TranscriberProviderCRUD:
    """
    Get or create the singleton TranscriberProviderCRUD instance.
    
    Returns:
        TranscriberProviderCRUD instance
    """
    global _transcriber_provider_crud_instance
    if _transcriber_provider_crud_instance is None:
        _transcriber_provider_crud_instance = TranscriberProviderCRUD()
    return _transcriber_provider_crud_instance
