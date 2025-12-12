"""
Memory schemas for toy memory and agent memory
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# ============================================================================
# TOY MEMORY SCHEMAS
# ============================================================================

class ToyMemoryBase(BaseModel):
    """Base schema for toy memory"""
    toy_id: UUID = Field(..., description="UUID of the toy")
    content_type: Optional[str] = Field(None, description="Type of content (e.g., conversation, document)")
    chunk_text: str = Field(..., description="Text content of the chunk")
    chunk_index: Optional[int] = Field(None, description="Index of chunk in sequence")


class ToyMemoryCreate(ToyMemoryBase):
    """Schema for creating toy memory"""
    embedding_vector: Optional[List[float]] = Field(None, description="384-dimensional embedding vector")


class ToyMemoryUpdate(BaseModel):
    """Schema for updating toy memory"""
    content_type: Optional[str] = None
    chunk_text: Optional[str] = None
    chunk_index: Optional[int] = None
    embedding_vector: Optional[List[float]] = None


class ToyMemoryResponse(ToyMemoryBase):
    """Schema for toy memory response"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    embedding_vector: Optional[List[float]] = Field(None, description="384-dimensional embedding vector")

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# AGENT MEMORY SCHEMAS
# ============================================================================

class AgentMemoryBase(BaseModel):
    """Base schema for agent memory"""
    toy_id: UUID = Field(..., description="UUID of the toy")
    agent_id: UUID = Field(..., description="UUID of the agent")
    original_filename: Optional[str] = Field(None, description="Original filename if from file upload")
    storage_file_id: Optional[str] = Field(None, description="Storage file identifier")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    content_type: Optional[str] = Field(None, description="MIME type of content")
    chunk_text: str = Field(..., description="Text content of the chunk")
    chunk_index: Optional[int] = Field(None, description="Index of chunk in sequence")


class AgentMemoryCreate(AgentMemoryBase):
    """Schema for creating agent memory"""
    embedding_vector: Optional[List[float]] = Field(None, description="384-dimensional embedding vector")


class AgentMemoryUpdate(BaseModel):
    """Schema for updating agent memory"""
    original_filename: Optional[str] = None
    storage_file_id: Optional[str] = None
    file_size: Optional[int] = None
    content_type: Optional[str] = None
    chunk_text: Optional[str] = None
    chunk_index: Optional[int] = None
    embedding_vector: Optional[List[float]] = None


class AgentMemoryResponse(AgentMemoryBase):
    """Schema for agent memory response"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    embedding_vector: Optional[List[float]] = Field(None, description="384-dimensional embedding vector")

    model_config = ConfigDict(from_attributes=True)
