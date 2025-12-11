"""
API v1 module
"""
from fastapi import APIRouter
from app.api.v1 import (
    routes_conversation_memory
)

# Create main v1 router
router = APIRouter(prefix="/api/v1")

# Include all v1 routes
router.include_router(routes_conversation_memory.router, tags=["conversation-memory"])

__all__ = ["router"]
