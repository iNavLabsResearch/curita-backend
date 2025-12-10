"""
Base Call Session Handler

Base implementation for call session handlers.
"""

from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime

from app.media_stream_handler.icall_session_handler import ICallSessionHandler
from app.telemetries.logger import logger


class BaseCallSessionHandler(ICallSessionHandler):
    """
    Base call session handler implementation
    """
    
    def __init__(self):
        """Initialize handler"""
        self.sessions: Dict[UUID, Dict[str, Any]] = {}
        logger.info(f"{self.__class__.__name__} initialized")
    
    async def start_session(self, session_id: UUID, config: Dict[str, Any]) -> None:
        """Start a new session"""
        logger.info(f"Starting session: {session_id}")
        
        self.sessions[session_id] = {
            "id": session_id,
            "config": config,
            "started_at": datetime.utcnow(),
            "state": "active",
            "audio_chunks_received": 0,
            "audio_chunks_sent": 0
        }
        
        logger.info(f"Session {session_id} started successfully")
    
    async def handle_audio(self, session_id: UUID, audio_data: bytes) -> Optional[bytes]:
        """Handle incoming audio"""
        if session_id not in self.sessions:
            logger.warning(f"Session not found: {session_id}")
            return None
        
        session = self.sessions[session_id]
        session["audio_chunks_received"] += 1
        
        logger.debug(f"Received audio chunk for session {session_id}: {len(audio_data)} bytes")
        
        # TODO: Process audio
        # TODO: Generate response
        
        return None
    
    async def end_session(self, session_id: UUID) -> None:
        """End session"""
        if session_id not in self.sessions:
            logger.warning(f"Session not found: {session_id}")
            return
        
        session = self.sessions[session_id]
        session["state"] = "ended"
        session["ended_at"] = datetime.utcnow()
        
        logger.info(f"Session {session_id} ended. Stats: {session['audio_chunks_received']} chunks received")
        
        # Clean up
        del self.sessions[session_id]
    
    async def get_session_state(self, session_id: UUID) -> Dict[str, Any]:
        """Get session state"""
        if session_id not in self.sessions:
            return {"error": "Session not found"}
        
        return self.sessions[session_id].copy()
