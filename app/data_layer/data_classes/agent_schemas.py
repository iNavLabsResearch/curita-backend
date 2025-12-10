"""
Agent schemas for agent entities and tools
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


# ============================================================================
# AGENT SCHEMAS
# ============================================================================

class AgentBase(BaseModel):
    """Base schema for agent"""
    toy_id: UUID
    name: str
    system_prompt: str
    model_provider_id: Optional[UUID] = None
    tts_provider_id: Optional[UUID] = None
    transcriber_provider_id: Optional[UUID] = None
    voice_id: Optional[str] = None
    language_code: str = "en-US"
    is_active: bool = True


class AgentCreate(AgentBase):
    """Schema for creating agent"""
    pass


class AgentUpdate(BaseModel):
    """Schema for updating agent"""
    name: Optional[str] = None
    system_prompt: Optional[str] = None
    model_provider_id: Optional[UUID] = None
    tts_provider_id: Optional[UUID] = None
    transcriber_provider_id: Optional[UUID] = None
    voice_id: Optional[str] = None
    language_code: Optional[str] = None
    is_active: Optional[bool] = None


class AgentResponse(AgentBase):
    """Schema for agent response"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# AGENT TOOLS SCHEMAS
# ============================================================================

class AgentToolBase(BaseModel):
    """Base schema for agent tool"""
    toy_id: UUID
    name: str
    url: str
    headers_schema: Dict[str, Any] = {}
    payload_schema: Optional[Dict[str, Any]] = None
    tool_schema: Dict[str, Any]
    http_method: str = "POST"
    provider_name: Optional[str] = None
    output_schema: Optional[Dict[str, Any]] = None


class AgentToolCreate(AgentToolBase):
    """Schema for creating agent tool"""
    pass


class AgentToolUpdate(BaseModel):
    """Schema for updating agent tool"""
    name: Optional[str] = None
    url: Optional[str] = None
    headers_schema: Optional[Dict[str, Any]] = None
    payload_schema: Optional[Dict[str, Any]] = None
    tool_schema: Optional[Dict[str, Any]] = None
    http_method: Optional[str] = None
    provider_name: Optional[str] = None
    output_schema: Optional[Dict[str, Any]] = None


class AgentToolResponse(AgentToolBase):
    """Schema for agent tool response"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
