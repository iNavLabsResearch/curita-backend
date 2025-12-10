"""
Domain models for conversation
"""
from enum import Enum


class MessageRole(str, Enum):
    """Roles in conversation"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"
