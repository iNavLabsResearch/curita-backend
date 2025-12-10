"""
Conversation History

Manages conversation history for toy interactions.
"""

from typing import Dict, Any, List, Optional
from uuid import UUID
from datetime import datetime
from dataclasses import dataclass, field

from app.telemetries.logger import logger


@dataclass
class ConversationMessage:
    """Single message in conversation"""
    message_id: str
    toy_id: UUID
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "message_id": self.message_id,
            "toy_id": str(self.toy_id),
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


class ConversationHistory:
    """
    Manages conversation history for a toy
    """
    
    def __init__(self, toy_id: UUID, max_length: int = 50):
        """
        Initialize conversation history
        
        Args:
            toy_id: Toy identifier
            max_length: Maximum number of messages to keep in memory
        """
        self.toy_id = toy_id
        self.max_length = max_length
        self.messages: List[ConversationMessage] = []
        self.session_start: Optional[datetime] = None
        self.session_end: Optional[datetime] = None
        
        logger.info(f"Initialized conversation history for toy: {toy_id}")
    
    def add_message(
        self, 
        role: str, 
        content: str, 
        message_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ConversationMessage:
        """
        Add message to history
        
        Args:
            role: Message role ('user' or 'assistant')
            content: Message content
            message_id: Optional message identifier
            metadata: Optional message metadata
            
        Returns:
            Created message
        """
        from uuid import uuid4
        
        if message_id is None:
            message_id = str(uuid4())
        
        message = ConversationMessage(
            message_id=message_id,
            toy_id=self.toy_id,
            role=role,
            content=content,
            metadata=metadata or {}
        )
        
        self.messages.append(message)
        
        # Trim history if it exceeds max length
        if len(self.messages) > self.max_length:
            removed = self.messages.pop(0)
            logger.debug(f"Removed oldest message: {removed.message_id}")
        
        logger.debug(f"Added {role} message to history (total: {len(self.messages)})")
        
        return message
    
    def get_recent_messages(self, count: int = 10) -> List[ConversationMessage]:
        """
        Get recent messages
        
        Args:
            count: Number of recent messages to retrieve
            
        Returns:
            List of recent messages
        """
        return self.messages[-count:] if len(self.messages) > count else self.messages
    
    def get_all_messages(self) -> List[ConversationMessage]:
        """
        Get all messages in history
        
        Returns:
            All messages
        """
        return self.messages.copy()
    
    def get_context_window(self, window_size: int = 10) -> List[Dict[str, str]]:
        """
        Get context window for LLM
        
        Args:
            window_size: Number of messages for context
            
        Returns:
            List of message dictionaries with role and content
        """
        recent = self.get_recent_messages(window_size)
        return [
            {"role": msg.role, "content": msg.content}
            for msg in recent
        ]
    
    def clear_history(self) -> None:
        """Clear all messages from history"""
        message_count = len(self.messages)
        self.messages.clear()
        logger.info(f"Cleared {message_count} messages from history for toy {self.toy_id}")
    
    def start_session(self) -> None:
        """Mark session start"""
        self.session_start = datetime.utcnow()
        logger.info(f"Started conversation session for toy {self.toy_id}")
    
    def end_session(self) -> None:
        """Mark session end"""
        self.session_end = datetime.utcnow()
        logger.info(f"Ended conversation session for toy {self.toy_id}")
    
    def get_session_duration(self) -> Optional[float]:
        """
        Get session duration in seconds
        
        Returns:
            Duration in seconds or None if session not started
        """
        if not self.session_start:
            return None
        
        end_time = self.session_end or datetime.utcnow()
        duration = (end_time - self.session_start).total_seconds()
        return duration
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get conversation statistics
        
        Returns:
            Statistics dictionary
        """
        user_messages = sum(1 for msg in self.messages if msg.role == "user")
        assistant_messages = sum(1 for msg in self.messages if msg.role == "assistant")
        
        return {
            "toy_id": str(self.toy_id),
            "total_messages": len(self.messages),
            "user_messages": user_messages,
            "assistant_messages": assistant_messages,
            "session_active": self.session_end is None and self.session_start is not None,
            "session_start": self.session_start.isoformat() if self.session_start else None,
            "session_end": self.session_end.isoformat() if self.session_end else None,
            "session_duration_seconds": self.get_session_duration()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert history to dictionary
        
        Returns:
            History as dictionary
        """
        return {
            "toy_id": str(self.toy_id),
            "max_length": self.max_length,
            "messages": [msg.to_dict() for msg in self.messages],
            "statistics": self.get_statistics()
        }
