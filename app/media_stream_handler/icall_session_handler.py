"""
Call Session Handler Interface

Interface for call session handlers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from uuid import UUID

from app.telemetries.logger import logger


class ICallSessionHandler(ABC):
    """
    Interface for call session handlers
    """
    
    @abstractmethod
    async def start_session(self, session_id: UUID, config: Dict[str, Any]) -> None:
        """
        Start a new session
        
        Args:
            session_id: Session identifier
            config: Session configuration
        """
        pass
    
    @abstractmethod
    async def handle_audio(self, session_id: UUID, audio_data: bytes) -> Optional[bytes]:
        """
        Handle incoming audio
        
        Args:
            session_id: Session identifier
            audio_data: Audio data bytes
            
        Returns:
            Response audio or None
        """
        pass
    
    @abstractmethod
    async def end_session(self, session_id: UUID) -> None:
        """
        End session
        
        Args:
            session_id: Session identifier
        """
        pass
    
    @abstractmethod
    async def get_session_state(self, session_id: UUID) -> Dict[str, Any]:
        """
        Get session state
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session state dictionary
        """
        pass
