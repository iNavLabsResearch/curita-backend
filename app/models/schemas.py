"""
Pydantic schemas for request/response models
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID


# Base schemas
class BaseResponse(BaseModel):
    """Base response model"""
    success: bool
    message: Optional[str] = None


class PaginationParams(BaseModel):
    """Pagination parameters"""
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)


# ============================================================================
# PROVIDER SCHEMAS
# ============================================================================

class ModelProviderBase(BaseModel):
    """Base schema for model provider"""
    provider_name: str
    model_name: str
    is_large_model: bool = False
    default_temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    supported_languages: List[str] = ["en"]
    api_key_template: Optional[str] = None
    api_base: Optional[str] = None
    api_key: Optional[str] = None
    is_default: bool = False


class ModelProviderCreate(ModelProviderBase):
    """Schema for creating model provider"""
    pass


class ModelProviderUpdate(BaseModel):
    """Schema for updating model provider"""
    provider_name: Optional[str] = None
    model_name: Optional[str] = None
    is_large_model: Optional[bool] = None
    default_temperature: Optional[float] = None
    supported_languages: Optional[List[str]] = None
    api_key_template: Optional[str] = None
    api_base: Optional[str] = None
    api_key: Optional[str] = None
    is_default: Optional[bool] = None


class ModelProviderResponse(ModelProviderBase):
    """Schema for model provider response"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TTSProviderBase(BaseModel):
    """Base schema for TTS provider"""
    provider_name: str
    model_name: str
    supported_languages: List[str] = ["en"]
    requires_api_key: bool = True
    default_endpoint: Optional[str] = None
    api_key_template: Optional[str] = None
    api_key: Optional[str] = None
    is_default: bool = False
    default_voice: Optional[str] = None


class TTSProviderCreate(TTSProviderBase):
    """Schema for creating TTS provider"""
    pass


class TTSProviderUpdate(BaseModel):
    """Schema for updating TTS provider"""
    provider_name: Optional[str] = None
    model_name: Optional[str] = None
    supported_languages: Optional[List[str]] = None
    requires_api_key: Optional[bool] = None
    default_endpoint: Optional[str] = None
    api_key_template: Optional[str] = None
    api_key: Optional[str] = None
    is_default: Optional[bool] = None
    default_voice: Optional[str] = None


class TTSProviderResponse(TTSProviderBase):
    """Schema for TTS provider response"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TranscriberProviderBase(BaseModel):
    """Base schema for transcriber provider"""
    name: Optional[str] = None
    provider_name: str
    model_name: str
    supported_languages: List[str] = ["en"]
    requires_api_key: bool = True
    default_endpoint: Optional[str] = None
    api_key_template: Optional[str] = None
    model_size: Optional[str] = None
    is_default: bool = False
    api_key: Optional[str] = None


class TranscriberProviderCreate(TranscriberProviderBase):
    """Schema for creating transcriber provider"""
    pass


class TranscriberProviderUpdate(BaseModel):
    """Schema for updating transcriber provider"""
    name: Optional[str] = None
    provider_name: Optional[str] = None
    model_name: Optional[str] = None
    supported_languages: Optional[List[str]] = None
    requires_api_key: Optional[bool] = None
    default_endpoint: Optional[str] = None
    api_key_template: Optional[str] = None
    model_size: Optional[str] = None
    is_default: Optional[bool] = None
    api_key: Optional[str] = None


class TranscriberProviderResponse(TranscriberProviderBase):
    """Schema for transcriber provider response"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# TOY SCHEMAS
# ============================================================================

class ToyBase(BaseModel):
    """Base schema for toy"""
    name: str
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    user_custom_instruction: Optional[str] = None
    is_active: bool = True


class ToyCreate(ToyBase):
    """Schema for creating toy"""
    pass


class ToyUpdate(BaseModel):
    """Schema for updating toy"""
    name: Optional[str] = None
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    user_custom_instruction: Optional[str] = None
    is_active: Optional[bool] = None


class ToyResponse(ToyBase):
    """Schema for toy response"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


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


# ============================================================================
# MEMORY SCHEMAS
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


# ============================================================================
# CONVERSATION SCHEMAS
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


class MessageCitationBase(BaseModel):
    """Base schema for message citation"""
    log_id: UUID
    toy_memory_id: Optional[UUID] = None
    agent_memory_id: Optional[UUID] = None
    similarity_score: Optional[float] = None


class MessageCitationCreate(MessageCitationBase):
    """Schema for creating message citation"""
    pass


class MessageCitationResponse(MessageCitationBase):
    """Schema for message citation response"""
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# API REQUEST/RESPONSE SCHEMAS
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


class ConversationStartRequest(BaseModel):
    """Request to start a conversation"""
    agent_id: UUID
    initial_message: Optional[str] = None


class SendMessageRequest(BaseModel):
    """Request to send a message"""
    agent_id: UUID
    message: str
    include_citations: bool = True


class MessageWithCitations(BaseModel):
    """Message with its citations"""
    log: ConversationLogResponse
    citations: List[MessageCitationResponse] = []


class ConversationHistoryResponse(BaseResponse):
    """Response with conversation history"""
    agent_id: UUID
    messages: List[MessageWithCitations]
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


class ListResponse(BaseResponse):
    """Generic list response"""
    items: List[Any]
    count: int
    limit: int
    offset: int


# Legacy document schemas (keeping for backward compatibility)
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
