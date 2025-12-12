"""
CRUD module initialization - exports all CRUD classes and singleton getters
"""
# Base CRUD
from app.data_layer.crud.base_crud import BaseCRUD

# Toy CRUD
from app.data_layer.crud.toy_crud import ToyCRUD, get_toy_crud

# Agent CRUD
from app.data_layer.crud.agent_crud import AgentCRUD, get_agent_crud

# Agent Tool CRUD
from app.data_layer.crud.agent_tool_crud import AgentToolCRUD, get_agent_tool_crud

# Provider CRUDs
from app.data_layer.crud.model_provider_crud import (
    ModelProviderCRUD,
    get_model_provider_crud,
)
from app.data_layer.crud.tts_provider_crud import (
    TTSProviderCRUD,
    get_tts_provider_crud,
)
from app.data_layer.crud.transcriber_provider_crud import (
    TranscriberProviderCRUD,
    get_transcriber_provider_crud,
)

# Memory CRUDs
from app.data_layer.crud.memory_crud import (
    ToyMemoryCRUD,
    AgentMemoryCRUD,
    get_toy_memory_crud,
    get_agent_memory_crud,
)

# Conversation CRUDs
from app.data_layer.crud.conversation_crud import (
    ConversationLogCRUD,
    MessageCitationCRUD,
    get_conversation_log_crud,
    get_message_citation_crud,
    get_message_with_citations,
)

__all__ = [
    # Base
    "BaseCRUD",
    
    # Toy
    "ToyCRUD",
    "get_toy_crud",
    
    # Agent
    "AgentCRUD",
    "get_agent_crud",
    
    # Agent Tool
    "AgentToolCRUD",
    "get_agent_tool_crud",
    
    # Providers
    "ModelProviderCRUD",
    "TTSProviderCRUD",
    "TranscriberProviderCRUD",
    "get_model_provider_crud",
    "get_tts_provider_crud",
    "get_transcriber_provider_crud",
    
    # Memory
    "ToyMemoryCRUD",
    "AgentMemoryCRUD",
    "get_toy_memory_crud",
    "get_agent_memory_crud",
    
    # Conversation
    "ConversationLogCRUD",
    "MessageCitationCRUD",
    "get_conversation_log_crud",
    "get_message_citation_crud",
    "get_message_with_citations",
]

