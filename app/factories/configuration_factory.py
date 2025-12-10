"""
Configuration Factory

Factory for creating configuration objects.
"""

from typing import Dict, Any
from uuid import UUID

from app.toys_management.domain_models.toy_configuration import ToyConfiguration
from app.telemetries.logger import logger


class ConfigurationFactory:
    """
    Factory for creating configuration objects
    """
    
    @staticmethod
    def create_toy_configuration(toy_id: UUID, config_data: Dict[str, Any]) -> ToyConfiguration:
        """
        Create toy configuration from data
        
        Args:
            toy_id: Toy identifier
            config_data: Configuration data
            
        Returns:
            ToyConfiguration instance
        """
        logger.info(f"Creating toy configuration for: {toy_id}")
        
        try:
            config = ToyConfiguration.from_dict({
                "toy_id": toy_id,
                **config_data
            })
            logger.info(f"Toy configuration created successfully for: {toy_id}")
            return config
        except Exception as e:
            logger.error(f"Error creating toy configuration: {e}")
            raise
    
    @staticmethod
    def create_default_toy_configuration(toy_id: UUID, name: str) -> ToyConfiguration:
        """
        Create default toy configuration
        
        Args:
            toy_id: Toy identifier
            name: Toy name
            
        Returns:
            ToyConfiguration with default values
        """
        logger.info(f"Creating default toy configuration for: {name}")
        
        return ToyConfiguration.from_dict({
            "toy_id": str(toy_id),
            "name": name,
            "personality": "friendly",
            "audio": {
                "sample_rate": 16000,
                "channels": 1,
                "format": "pcm",
                "codec": "opus"
            },
            "voice": {
                "provider": "openai",
                "voice_name": "default",
                "language": "en-US"
            },
            "conversation": {
                "max_history_length": 50,
                "enable_memory": True
            }
        })
    
    @staticmethod
    def validate_configuration(config: ToyConfiguration) -> tuple[bool, list[str]]:
        """
        Validate toy configuration
        
        Args:
            config: Configuration to validate
            
        Returns:
            Tuple of (is_valid, list of errors)
        """
        errors = []
        
        if not config.name:
            errors.append("Toy name is required")
        
        if config.audio.sample_rate <= 0:
            errors.append("Invalid audio sample rate")
        
        if config.conversation.max_history_length <= 0:
            errors.append("Invalid max history length")
        
        is_valid = len(errors) == 0
        
        if not is_valid:
            logger.warning(f"Configuration validation failed: {errors}")
        
        return is_valid, errors
