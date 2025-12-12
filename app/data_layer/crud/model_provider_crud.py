"""
CRUD operations for Model Provider entities.
Provides database operations for managing LLM providers in the system.
"""
from typing import Optional, List
from uuid import UUID
from app.data_layer.crud.base_crud import BaseCRUD
from app.data_layer.data_classes.provider_schemas import (
    ModelProviderCreate,
    ModelProviderUpdate,
    ModelProviderResponse
)
from app.data_layer.supabase_client import SupabaseClient
from app.telemetries.logger import logger


class ModelProviderCRUD(BaseCRUD[ModelProviderCreate, ModelProviderUpdate, ModelProviderResponse]):
    """
    CRUD operations for Model Provider entities.
    
    Handles all database operations related to model providers including:
    - Basic CRUD operations (inherited from BaseCRUD)
    - Default provider queries
    - Language-specific queries
    - Large model filtering
    """
    
    def __init__(self, supabase_client: Optional[SupabaseClient] = None):
        """
        Initialize ModelProviderCRUD instance.
        
        Args:
            supabase_client: Optional Supabase client instance
        """
        super().__init__(
            table_name="model_providers",
            response_model=ModelProviderResponse,
            supabase_client=supabase_client
        )
    
    async def get_default(self) -> Optional[ModelProviderResponse]:
        """
        Retrieve the default model provider.
        
        Returns:
            Default model provider record if found, None otherwise
        """
        try:
            logger.debug("Fetching default model provider")
            
            result = await self.supabase.select(
                self.table_name,
                filters={"is_default": True},
                limit=1,
                order_by="created_at",
                order_desc=False
            )
            
            if result and len(result) > 0:
                logger.info("Successfully retrieved default model provider")
                return self.response_model(**result[0])
            
            logger.warning("No default model provider found")
            return None
            
        except Exception as e:
            logger.error(f"Error fetching default model provider: {str(e)}", exc_info=True)
            return None
    
    async def get_by_provider_name(
        self,
        provider_name: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[ModelProviderResponse]:
        """
        Retrieve all model providers by provider name.
        
        Args:
            provider_name: Name of the provider (e.g., 'openai', 'anthropic')
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of model provider records
        """
        try:
            logger.debug(f"Fetching model providers for provider_name: {provider_name}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"provider_name": provider_name},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching model providers for provider_name {provider_name}: {str(e)}", exc_info=True)
            return []
    
    async def get_large_models(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[ModelProviderResponse]:
        """
        Retrieve all large model providers.
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of large model provider records
        """
        try:
            logger.debug("Fetching large model providers")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"is_large_model": True},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching large model providers: {str(e)}", exc_info=True)
            return []
    
    async def set_default(self, id: UUID) -> Optional[ModelProviderResponse]:
        """
        Set a model provider as the default.
        This will unset any existing default provider.
        
        Args:
            id: UUID of the provider to set as default
            
        Returns:
            Updated provider record if successful, None otherwise
        """
        try:
            logger.debug(f"Setting model provider {id} as default")
            
            # First, unset all existing defaults
            all_providers = await self.get_all(filters={"is_default": True}, limit=1000)
            for provider in all_providers:
                await self.update(provider.id, ModelProviderUpdate(is_default=False))
            
            # Set the new default
            update_data = ModelProviderUpdate(is_default=True)
            result = await self.update(id, update_data)
            
            if result:
                logger.info(f"Successfully set model provider {id} as default")
            
            return result
            
        except Exception as e:
            logger.error(f"Error setting default model provider {id}: {str(e)}", exc_info=True)
            return None


# Singleton instance for easy access
_model_provider_crud_instance: Optional[ModelProviderCRUD] = None


def get_model_provider_crud() -> ModelProviderCRUD:
    """
    Get or create the singleton ModelProviderCRUD instance.
    
    Returns:
        ModelProviderCRUD instance
    """
    global _model_provider_crud_instance
    if _model_provider_crud_instance is None:
        _model_provider_crud_instance = ModelProviderCRUD()
    return _model_provider_crud_instance
