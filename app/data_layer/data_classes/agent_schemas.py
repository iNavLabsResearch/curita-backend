"""
Agent schemas for agent entities and tools
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


# ============================================================================
# AGENT SCHEMAS
# ============================================================================

class AgentBase(BaseModel):
    """Base schema for agent"""
    toy_id: UUID = Field(..., description="UUID of the parent toy")
    name: str = Field(..., description="Name of the agent")
    system_prompt: str = Field(..., description="System prompt for the agent")
    model_provider_id: Optional[UUID] = Field(None, description="UUID of the model provider")
    tts_provider_id: Optional[UUID] = Field(None, description="UUID of the TTS provider")
    transcriber_provider_id: Optional[UUID] = Field(None, description="UUID of the transcriber provider")
    voice_id: Optional[str] = Field(None, description="Voice ID for TTS")
    language_code: str = Field("en-US", description="Language code (e.g., en-US)")
    is_active: bool = Field(True, description="Whether the agent is active")


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
    toy_id: UUID = Field(..., description="UUID of the toy")
    name: str = Field(..., description="Name of the tool")
    url: str = Field(..., description="API endpoint URL for the tool")
    headers_schema: Dict[str, Any] = Field(default={}, description="HTTP headers schema")
    payload_schema: Optional[Dict[str, Any]] = Field(None, description="Payload schema for the tool")
    tool_schema: Dict[str, Any] = Field(..., description="Tool function schema")
    http_method: str = Field("POST", description="HTTP method (GET, POST, etc.)")
    provider_name: Optional[str] = Field(None, description="Tool provider name")
    output_schema: Optional[Dict[str, Any]] = Field(None, description="Expected output schema")


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
