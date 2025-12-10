"""
Provider factory for dynamic provider creation
"""
from typing import Optional, Dict, Any
from uuid import UUID

from app.telemetries.logger import logger
from app.data_layer.domain_models.provider_types import ProviderType


class ProviderFactory:
    """
    Factory for creating provider instances dynamically
    
    Supports model, TTS, and transcriber providers
    """
    
    @staticmethod
    def create_model_provider(provider_config: Dict[str, Any]):
        """
        Create LLM model provider instance
        
        Args:
            provider_config: Provider configuration dictionary
            
        Returns:
            Model provider instance
        """
        provider_name = provider_config.get("provider_name", "").lower()
        logger.info(f"Creating model provider: {provider_name}")
        
        # TODO: Implement provider instantiation based on name
        # - OpenAI
        # - Anthropic
        # - Google
        # - Azure
        # - etc.
        
        return {
            "provider_name": provider_name,
            "model_name": provider_config.get("model_name"),
            "type": ProviderType.MODEL,
            "config": provider_config
        }
    
    @staticmethod
    def create_tts_provider(provider_config: Dict[str, Any]):
        """
        Create TTS provider instance
        
        Args:
            provider_config: Provider configuration dictionary
            
        Returns:
            TTS provider instance
        """
        provider_name = provider_config.get("provider_name", "").lower()
        logger.info(f"Creating TTS provider: {provider_name}")
        
        # TODO: Implement TTS provider instantiation
        # - ElevenLabs
        # - Cartesia
        # - Azure TTS
        # - Google TTS
        # - etc.
        
        return {
            "provider_name": provider_name,
            "model_name": provider_config.get("model_name"),
            "type": ProviderType.TTS,
            "config": provider_config
        }
    
    @staticmethod
    def create_transcriber_provider(provider_config: Dict[str, Any]):
        """
        Create transcriber (STT) provider instance
        
        Args:
            provider_config: Provider configuration dictionary
            
        Returns:
            Transcriber provider instance
        """
        provider_name = provider_config.get("provider_name", "").lower()
        logger.info(f"Creating transcriber provider: {provider_name}")
        
        # TODO: Implement transcriber provider instantiation
        # - Deepgram
        # - Whisper
        # - Azure STT
        # - Google STT
        # - etc.
        
        return {
            "provider_name": provider_name,
            "model_name": provider_config.get("model_name"),
            "type": ProviderType.TRANSCRIBER,
            "config": provider_config
        }
    
    @staticmethod
    def create_provider(provider_type: ProviderType, provider_config: Dict[str, Any]):
        """
        Create provider of any type
        
        Args:
            provider_type: Type of provider to create
            provider_config: Provider configuration dictionary
            
        Returns:
            Provider instance
        """
        logger.debug(f"Creating provider of type: {provider_type}")
        
        if provider_type == ProviderType.MODEL:
            return ProviderFactory.create_model_provider(provider_config)
        elif provider_type == ProviderType.TTS:
            return ProviderFactory.create_tts_provider(provider_config)
        elif provider_type == ProviderType.TRANSCRIBER:
            return ProviderFactory.create_transcriber_provider(provider_config)
        else:
            raise ValueError(f"Unknown provider type: {provider_type}")
