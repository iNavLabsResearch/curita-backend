"""
Conversation schemas for conversation logs and citations
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# ============================================================================
# CONVERSATION LOG SCHEMAS
# ============================================================================

class ConversationLogBase(BaseModel):
    """Base schema for conversation log"""
    agent_id: UUID
    role: str = Field(..., pattern="^(user|assistant|system|tool)$")
    content: Optional[str] = None


class ConversationLogCreate(ConversationLogBase):
    """Schema for creating conversation log"""
    pass


class ConversationLogResponse(ConversationLogBase):
    """Schema for conversation log response"""
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# MESSAGE CITATION SCHEMAS
# ============================================================================

class MessageCitationBase(BaseModel):
    """Base schema for message citation"""
    log_id: UUID = Field(..., description="UUID of the conversation log")
    toy_memory_id: Optional[UUID] = Field(None, description="UUID of toy memory (if citation is from toy memory)")
    agent_memory_id: Optional[UUID] = Field(None, description="UUID of agent memory (if citation is from agent memory)")
    similarity_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Similarity score (0-1)")


class MessageCitationCreate(MessageCitationBase):
    """Schema for creating message citation"""
    pass


class MessageCitationResponse(MessageCitationBase):
    """Schema for message citation response"""
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# COMPOSITE SCHEMAS
# ============================================================================

class MessageWithCitations(BaseModel):
    """Message with its citations"""
    log: ConversationLogResponse
    citations: List[MessageCitationResponse] = []
