"""
Domain models for memory types
"""
from enum import Enum


class MemoryType(str, Enum):
    """Types of memory in the system"""
    TOY_MEMORY = "toy_memory"  # Short-term interaction context
    AGENT_MEMORY = "agent_memory"  # Long-term knowledge base


class ContentType(str, Enum):
    """Content types for memory"""
    TEXT = "text"
    DOCUMENT = "document"
    CONVERSATION = "conversation"
    CONTEXT = "context"
