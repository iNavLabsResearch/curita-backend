"""
API request/response schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID

from app.data_layer.data_classes.base_schemas import BaseResponse


# ============================================================================
# TEXT-TO-MEMORY API SCHEMAS (STT Pipeline)
# ============================================================================

class TextToMemoryRequest(BaseModel):
    """Request to process extracted text from STT to memory"""
    text: str = Field(..., min_length=1, description="Extracted text from STT")
    toy_id: UUID = Field(..., description="UUID of the toy")
    agent_id: UUID = Field(..., description="UUID of the agent")
    role: str = Field(default="user", pattern="^(user|assistant|system|tool)$", description="Message role")
    content_type: Optional[str] = Field(default="conversation", description="Type of content")
    chunk_size: Optional[int] = Field(default=None, ge=100, le=4000, description="Custom chunk size")
    chunk_overlap: Optional[int] = Field(default=None, ge=0, le=1000, description="Custom chunk overlap")


class ChunkStatistics(BaseModel):
    """Statistics about chunks"""
    total_chunks: int
    total_characters: int
    avg_chunk_size: float
    min_chunk_size: int
    max_chunk_size: int


class TextToMemoryResponse(BaseResponse):
    """Response for text-to-memory processing"""
    conversation_log_id: UUID = Field(..., description="ID of created conversation log")
    toy_memory_ids: List[UUID] = Field(..., description="IDs of created toy memory chunks")
    chunks_stored: int = Field(..., description="Number of chunks stored")
    total_characters: int = Field(..., description="Total characters processed")
    chunk_statistics: ChunkStatistics = Field(..., description="Statistics about chunks")


class BatchTextToMemoryRequest(BaseModel):
    """Request to process multiple texts in batch"""
    texts: List[str] = Field(..., min_items=1, description="List of texts to process")
    toy_id: UUID = Field(..., description="UUID of the toy")
    agent_id: UUID = Field(..., description="UUID of the agent")
    role: str = Field(default="user", pattern="^(user|assistant|system|tool)$", description="Message role")


class BatchTextToMemoryResponse(BaseResponse):
    """Response for batch text-to-memory processing"""
    results: List[TextToMemoryResponse]
    total_processed: int
    total_chunks_stored: int


# ============================================================================
# MEMORY SEARCH API SCHEMAS
# ============================================================================


class MemorySearchResult(BaseModel):
    """Single memory search result"""
    id: UUID
    memory_type: str
    toy_id: Optional[UUID] = None
    agent_id: Optional[UUID] = None
    chunk_text: Optional[str] = None
    chunk_index: Optional[int] = None
    similarity: float
    metadata: Optional[dict] = None
    created_at: Optional[str] = None


class SearchMemoryRequest(BaseModel):
    """Request to search memory via Supabase RPC"""
    query_text: str = Field(..., min_length=1, description="User query text")
    toy_id: Optional[UUID] = Field(default=None, description="Filter by toy")
    agent_id: Optional[UUID] = Field(default=None, description="Filter by agent")
    match_count: int = Field(default=5, ge=1, le=50, description="Max results per page")
    offset: int = Field(default=0, ge=0, description="Pagination offset")
    similarity_threshold: float = Field(default=0.0, ge=0.0, le=1.0, description="Min similarity (0-1)")
    scope: str = Field(default="all", pattern="^(toy|agent|all)$", description="Search scope")


class SearchMemoryResponse(BaseResponse):
    """Response for memory search"""
    results: List[MemorySearchResult]
    total_results: int
    offset: int = 0
    limit: int = 5
    has_more: bool = False