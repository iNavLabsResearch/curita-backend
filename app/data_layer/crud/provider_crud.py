"""
CRUD operations for Providers (Model, TTS, Transcriber)
"""
from uuid import UUID
from typing import List, Optional
from app.data_layer.supabase_client import SupabaseClient
from app.data_layer.crud.base_crud import BaseCrud
from app.data_layer.data_classes.provider_schemas import (
    ModelProviderResponse,
    TTSProviderResponse,
    TranscriberProviderResponse,
)
from app.telemetries.logger import logger


class ModelProviderCRUD(BaseCrud):
    """CRUD operations for model_providers table"""
    
    def __init__(self, supabase: SupabaseClient):
        super().__init__(supabase, "model_providers", ModelProviderResponse)
    
    async def get_default_provider(self) -> Optional[ModelProviderResponse]:
        """
        Get the default model provider
        
        Returns:
            Default model provider or None
        """
        try:
            logger.debug("Fetching default model provider")
            results = await self.filter_by(is_default=True)
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Error fetching default model provider: {str(e)}")
            raise
    
    async def get_by_provider_name(self, provider_name: str) -> List[ModelProviderResponse]:
        """
        Get providers by provider name
        
        Args:
            provider_name: Name of the provider
            
        Returns:
            List of model providers
        """
        try:
            logger.debug(f"Fetching model providers by name: {provider_name}")
            return await self.filter_by(provider_name=provider_name)
        except Exception as e:
            logger.error(f"Error fetching model providers by name: {str(e)}")
            raise


class TTSProviderCRUD(BaseCrud):
    """CRUD operations for tts_providers table"""
    
    def __init__(self, supabase: SupabaseClient):
        super().__init__(supabase, "tts_providers", TTSProviderResponse)
    
    async def get_default_provider(self) -> Optional[TTSProviderResponse]:
        """
        Get the default TTS provider
        
        Returns:
            Default TTS provider or None
        """
        try:
            logger.debug("Fetching default TTS provider")
            results = await self.filter_by(is_default=True)
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Error fetching default TTS provider: {str(e)}")
            raise
    
    async def get_by_provider_name(self, provider_name: str) -> List[TTSProviderResponse]:
        """
        Get providers by provider name
        
        Args:
            provider_name: Name of the provider
            
        Returns:
            List of TTS providers
        """
        try:
            logger.debug(f"Fetching TTS providers by name: {provider_name}")
            return await self.filter_by(provider_name=provider_name)
        except Exception as e:
            logger.error(f"Error fetching TTS providers by name: {str(e)}")
            raise


class TranscriberProviderCRUD(BaseCrud):
    """CRUD operations for transcriber_providers table"""
    
    def __init__(self, supabase: SupabaseClient):
        super().__init__(supabase, "transcriber_providers", TranscriberProviderResponse)
    
    async def get_default_provider(self) -> Optional[TranscriberProviderResponse]:
        """
        Get the default transcriber provider
        
        Returns:
            Default transcriber provider or None
        """
        try:
            logger.debug("Fetching default transcriber provider")
            results = await self.filter_by(is_default=True)
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Error fetching default transcriber provider: {str(e)}")
            raise
    
    async def get_by_provider_name(self, provider_name: str) -> List[TranscriberProviderResponse]:
        """
        Get providers by provider name
        
        Args:
            provider_name: Name of the provider
            
        Returns:
            List of transcriber providers
        """
        try:
            logger.debug(f"Fetching transcriber providers by name: {provider_name}")
            return await self.filter_by(provider_name=provider_name)
        except Exception as e:
            logger.error(f"Error fetching transcriber providers by name: {str(e)}")
            raise

