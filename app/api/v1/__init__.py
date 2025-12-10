"""
API v1 module
"""
from fastapi import APIRouter
from app.api.v1 import routes, routes_providers, routes_toys_agents, routes_memory

# Create main v1 router
router = APIRouter(prefix="/api/v1")

# Include all v1 routes
router.include_router(routes.router, tags=["documents"])
router.include_router(routes_providers.router, tags=["providers"])
router.include_router(routes_toys_agents.router, tags=["toys-agents"])
router.include_router(routes_memory.router, tags=["memory"])

__all__ = ["router"]
