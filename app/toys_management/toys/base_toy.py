"""
Base Toy Abstract Class

Defines the interface for toy implementations in the Curita platform.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from uuid import UUID
from datetime import datetime

from app.telemetries.logger import logger


class BaseToy(ABC):
    """
    Abstract base class for all toy implementations
    
    Provides the interface that all toy types must implement.
    """
    
    def __init__(self, toy_id: UUID, config: Dict[str, Any]):
        """
        Initialize base toy
        
        Args:
            toy_id: Unique identifier for the toy
            config: Toy configuration dictionary
        """
        self.toy_id = toy_id
        self.config = config
        self.name = config.get("name", "Unknown Toy")
        self.toy_type = config.get("toy_type", "generic")
        self.is_active = config.get("is_active", True)
        self.created_at = config.get("created_at", datetime.utcnow())
        self.metadata = config.get("metadata", {})
        
        logger.info(f"Initialized {self.__class__.__name__} with ID: {toy_id}")
    
    @abstractmethod
    async def initialize(self) -> None:
        """
        Initialize toy resources
        
        Called when toy is first created or loaded.
        """
        pass
    
    @abstractmethod
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming message from child
        
        Args:
            message: Message dictionary
            
        Returns:
            Response dictionary
        """
        pass
    
    @abstractmethod
    async def handle_audio_stream(self, audio_data: bytes) -> Optional[bytes]:
        """
        Process audio stream from toy microphone
        
        Args:
            audio_data: Raw audio bytes
            
        Returns:
            Processed audio response or None
        """
        pass
    
    @abstractmethod
    async def get_response(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate response to user input
        
        Args:
            user_input: User's text input
            context: Optional conversation context
            
        Returns:
            Generated response text
        """
        pass
    
    @abstractmethod
    async def save_interaction(self, interaction_data: Dict[str, Any]) -> None:
        """
        Save interaction to history
        
        Args:
            interaction_data: Interaction details
        """
        pass
    
    @abstractmethod
    async def get_state(self) -> Dict[str, Any]:
        """
        Get current toy state
        
        Returns:
            Current state dictionary
        """
        pass
    
    @abstractmethod
    async def cleanup(self) -> None:
        """
        Clean up toy resources
        
        Called when toy session ends.
        """
        pass
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get toy configuration
        
        Returns:
            Configuration dictionary
        """
        return self.config
    
    def update_config(self, updates: Dict[str, Any]) -> None:
        """
        Update toy configuration
        
        Args:
            updates: Configuration updates
        """
        self.config.update(updates)
        logger.info(f"Updated configuration for toy {self.toy_id}")
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.toy_id}, name={self.name}, type={self.toy_type})>"
