"""
API v1 module - Modular CRUD routes for all database tables
"""
from fastapi import APIRouter
from app.api.v1 import (
    routes_toy,
    routes_agent,
    routes_agent_tool,
    routes_model_provider,
    routes_tts_provider,
    routes_transcriber_provider,
    routes_memory,
    routes_conversation,
    routes_conversation_memory
)

# Create main v1 router
router = APIRouter(prefix="/api/v1")

# Include all CRUD routes (modular approach)
router.include_router(routes_toy.router)
router.include_router(routes_agent.router)
router.include_router(routes_agent_tool.router)
router.include_router(routes_model_provider.router)
router.include_router(routes_tts_provider.router)
router.include_router(routes_transcriber_provider.router)
router.include_router(routes_memory.toy_memory_router)
router.include_router(routes_memory.agent_memory_router)
router.include_router(routes_conversation.conversation_router)
router.include_router(routes_conversation.citation_router)

# Include legacy/specialized routes
router.include_router(routes_conversation_memory.router, tags=["conversation-memory"])

__all__ = ["router"]
