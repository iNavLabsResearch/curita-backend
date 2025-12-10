"""
Memory schemas for toy memory and agent memory
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


# ============================================================================
# TOY MEMORY SCHEMAS
# ============================================================================

class ToyMemoryBase(BaseModel):
    """Base schema for toy memory"""
    toy_id: UUID
    content_type: Optional[str] = None
    chunk_text: str
    chunk_index: Optional[int] = None


class ToyMemoryCreate(ToyMemoryBase):
    """Schema for creating toy memory"""
    pass


class ToyMemoryResponse(ToyMemoryBase):
    """Schema for toy memory response"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# AGENT MEMORY SCHEMAS
# ============================================================================

class AgentMemoryBase(BaseModel):
    """Base schema for agent memory"""
    toy_id: UUID
    agent_id: UUID
    original_filename: Optional[str] = None
    storage_file_id: Optional[str] = None
    file_size: Optional[int] = None
    content_type: Optional[str] = None
    chunk_text: str
    chunk_index: Optional[int] = None


class AgentMemoryCreate(AgentMemoryBase):
    """Schema for creating agent memory"""
    pass


class AgentMemoryResponse(AgentMemoryBase):
    """Schema for agent memory response"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
