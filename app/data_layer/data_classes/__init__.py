"""
Data classes initialization - All schemas organized by domain
"""
# Base schemas
from app.data_layer.data_classes.base_schemas import (
    BaseResponse,
    PaginationParams,
    ListResponse,
)

# Provider schemas
from app.data_layer.data_classes.provider_schemas import (
    ModelProviderBase,
    ModelProviderCreate,
    ModelProviderUpdate,
    ModelProviderResponse,
    TTSProviderBase,
    TTSProviderCreate,
    TTSProviderUpdate,
    TTSProviderResponse,
    TranscriberProviderBase,
    TranscriberProviderCreate,
    TranscriberProviderUpdate,
    TranscriberProviderResponse,
)

# Toy schemas
from app.data_layer.data_classes.toy_schemas import (
    ToyBase,
    ToyCreate,
    ToyUpdate,
    ToyResponse,
)

# Agent schemas
from app.data_layer.data_classes.agent_schemas import (
    AgentBase,
    AgentCreate,
    AgentUpdate,
    AgentResponse,
    AgentToolBase,
    AgentToolCreate,
    AgentToolUpdate,
    AgentToolResponse,
)

# Memory schemas
from app.data_layer.data_classes.memory_schemas import (
    ToyMemoryBase,
    ToyMemoryCreate,
    ToyMemoryResponse,
    AgentMemoryBase,
    AgentMemoryCreate,
    AgentMemoryResponse,
)

# Conversation schemas
from app.data_layer.data_classes.conversation_schemas import (
    ConversationLogBase,
    ConversationLogCreate,
    ConversationLogResponse,
    MessageCitationBase,
    MessageCitationCreate,
    MessageCitationResponse,
    MessageWithCitations,
)

# API schemas
from app.data_layer.data_classes.api_schemas import (
    MemorySearchRequest,
    MemorySearchResult,
    MemorySearchResponse,
    UploadToMemoryRequest,
    UploadToMemoryResponse,
    ConversationStartRequest,
    SendMessageRequest,
    ConversationHistoryResponse,
    DocumentMetadata,
    ChunkData,
    DocumentUploadResponse,
    SearchRequest,
    SearchByDocumentRequest,
    SearchResult,
    SearchResponse,
    UpdateChunkRequest,
    DocumentListResponse,
    DocumentDetailResponse,
    DeleteResponse,
    UpdateChunkResponse,
)

__all__ = [
    # Base
    "BaseResponse",
    "PaginationParams",
    "ListResponse",
    # Providers
    "ModelProviderBase",
    "ModelProviderCreate",
    "ModelProviderUpdate",
    "ModelProviderResponse",
    "TTSProviderBase",
    "TTSProviderCreate",
    "TTSProviderUpdate",
    "TTSProviderResponse",
    "TranscriberProviderBase",
    "TranscriberProviderCreate",
    "TranscriberProviderUpdate",
    "TranscriberProviderResponse",
    # Toys
    "ToyBase",
    "ToyCreate",
    "ToyUpdate",
    "ToyResponse",
    # Agents
    "AgentBase",
    "AgentCreate",
    "AgentUpdate",
    "AgentResponse",
    "AgentToolBase",
    "AgentToolCreate",
    "AgentToolUpdate",
    "AgentToolResponse",
    # Memory
    "ToyMemoryBase",
    "ToyMemoryCreate",
    "ToyMemoryResponse",
    "AgentMemoryBase",
    "AgentMemoryCreate",
    "AgentMemoryResponse",
    # Conversations
    "ConversationLogBase",
    "ConversationLogCreate",
    "ConversationLogResponse",
    "MessageCitationBase",
    "MessageCitationCreate",
    "MessageCitationResponse",
    "MessageWithCitations",
    # API
    "MemorySearchRequest",
    "MemorySearchResult",
    "MemorySearchResponse",
    "UploadToMemoryRequest",
    "UploadToMemoryResponse",
    "ConversationStartRequest",
    "SendMessageRequest",
    "ConversationHistoryResponse",
    "DocumentMetadata",
    "ChunkData",
    "DocumentUploadResponse",
    "SearchRequest",
    "SearchByDocumentRequest",
    "SearchResult",
    "SearchResponse",
    "UpdateChunkRequest",
    "DocumentListResponse",
    "DocumentDetailResponse",
    "DeleteResponse",
    "UpdateChunkResponse",
]

