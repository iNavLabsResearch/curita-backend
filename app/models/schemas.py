"""
Pydantic schemas for request/response models
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


# Base schemas
class BaseResponse(BaseModel):
    """Base response model"""
    success: bool
    message: Optional[str] = None


class PaginationParams(BaseModel):
    """Pagination parameters"""
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)


# Document schemas
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


# Search schemas
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


# CRUD schemas
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
