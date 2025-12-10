"""
API request/response schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

from app.data_layer.data_classes.base_schemas import BaseResponse
from app.data_layer.data_classes.conversation_schemas import MessageWithCitations


# ============================================================================
# MEMORY API SCHEMAS
# ============================================================================

class MemorySearchRequest(BaseModel):
    """Search request for memory"""
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=100)
    similarity_threshold: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    memory_type: Optional[str] = Field(default=None, pattern="^(toy|agent|both)$")
    toy_id: Optional[UUID] = None
    agent_id: Optional[UUID] = None


class MemorySearchResult(BaseModel):
    """Memory search result item"""
    id: UUID
    chunk_text: str
    chunk_index: Optional[int] = None
    similarity: float
    memory_type: str
    toy_id: UUID
    agent_id: Optional[UUID] = None
    created_at: datetime


class MemorySearchResponse(BaseResponse):
    """Memory search response"""
    query: str
    results: List[MemorySearchResult]
    count: int


class UploadToMemoryRequest(BaseModel):
    """Request to upload content to memory"""
    toy_id: UUID
    agent_id: Optional[UUID] = None
    content_type: Optional[str] = None
    chunk_size: int = Field(default=1000, ge=100, le=4000)
    chunk_overlap: int = Field(default=200, ge=0, le=1000)


class UploadToMemoryResponse(BaseResponse):
    """Response for memory upload"""
    memory_type: str
    toy_id: UUID
    agent_id: Optional[UUID] = None
    total_chunks: int
    stored_chunks: int


# ============================================================================
# CONVERSATION API SCHEMAS
# ============================================================================

class ConversationStartRequest(BaseModel):
    """Request to start a conversation"""
    agent_id: UUID
    initial_message: Optional[str] = None


class SendMessageRequest(BaseModel):
    """Request to send a message"""
    agent_id: UUID
    message: str
    include_citations: bool = True


class ConversationHistoryResponse(BaseResponse):
    """Response with conversation history"""
    agent_id: UUID
    messages: List[MessageWithCitations]
    count: int


# ============================================================================
# DOCUMENT API SCHEMAS (Legacy)
# ============================================================================

class DocumentMetadata(BaseModel):
    """Document metadata"""
    filename: str
    file_type: str
    total_chunks: int
    additional: Optional[Dict[str, Any]] = None


class ChunkData(BaseModel):
    """Chunk data model"""
    text: str
    chunk_index: int
    start_position: Optional[int] = None
    end_position: Optional[int] = None
    chunk_size: Optional[int] = None


class DocumentUploadResponse(BaseResponse):
    """Response for document upload"""
    document_id: str
    filename: str
    total_chunks: int
    stored_chunks: int


class SearchRequest(BaseModel):
    """Search request model"""
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=100)
    similarity_threshold: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    filter_metadata: Optional[Dict[str, Any]] = None


class SearchByDocumentRequest(BaseModel):
    """Search by document request model"""
    query: str = Field(..., min_length=1)
    document_id: str
    top_k: int = Field(default=5, ge=1, le=100)


class SearchResult(BaseModel):
    """Search result item"""
    id: int
    document_id: str
    chunk_text: str
    chunk_index: int
    metadata: Optional[Dict[str, Any]] = None
    similarity: float
    created_at: datetime


class SearchResponse(BaseResponse):
    """Search response model"""
    query: str
    results: List[Dict[str, Any]]
    count: int


class UpdateChunkRequest(BaseModel):
    """Update chunk request model"""
    chunk_text: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class DocumentListResponse(BaseResponse):
    """Document list response"""
    documents: List[Dict[str, Any]]
    count: int
    limit: int
    offset: int


class DocumentDetailResponse(BaseResponse):
    """Document detail response"""
    document_id: str
    chunks: List[Dict[str, Any]]
    total_chunks: int


class DeleteResponse(BaseResponse):
    """Delete response model"""
    document_id: str


class UpdateChunkResponse(BaseResponse):
    """Update chunk response"""
    chunk: Dict[str, Any]
