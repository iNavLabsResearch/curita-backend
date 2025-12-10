"""
Pydantic schemas for request/response models

NOTE: This file is kept for backward compatibility.
All schemas have been moved to app/data_layer/data_classes/
Import from there for new code.
"""

# Import all schemas from data_classes for backward compatibility
from app.data_layer.data_classes import *

# Explicitly list what's available (for IDE autocomplete)
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


