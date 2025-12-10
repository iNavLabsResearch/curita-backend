"""
API routes for toy and agent management
"""
from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from typing import List, Optional

from app.telemetries.logger import logger
from app.models.schemas import (
    ToyCreate, ToyUpdate, ToyResponse,
    AgentCreate, AgentUpdate, AgentResponse,
    AgentToolCreate, AgentToolUpdate, AgentToolResponse,
    BaseResponse
)
from app.services.toy_service import get_toy_service
from app.services.agent_service import get_agent_service
from app.services.agent_tools_service import get_agent_tools_service

router = APIRouter()


# ============================================================================
# TOY ROUTES
# ============================================================================

@router.post("/toys", response_model=ToyResponse, status_code=201)
async def create_toy(toy: ToyCreate):
    """Create a new toy"""
    logger.info(f"Creating toy: {toy.name}")
    try:
        service = get_toy_service()
        result = service.create(toy.model_dump())
        return result
    except Exception as e:
        logger.error(f"Error creating toy: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/toys", response_model=List[ToyResponse])
async def list_toys(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    is_active: Optional[bool] = None
):
    """List all toys"""
    logger.info(f"Listing toys: limit={limit}, offset={offset}, is_active={is_active}")
    try:
        service = get_toy_service()
        toys = service.list(limit=limit, offset=offset, is_active=is_active)
        return toys
    except Exception as e:
        logger.error(f"Error listing toys: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/toys/{toy_id}", response_model=ToyResponse)
async def get_toy(toy_id: UUID):
    """Get toy by ID"""
    logger.info(f"Fetching toy: {toy_id}")
    try:
        service = get_toy_service()
        toy = service.get_by_id(toy_id)
        if not toy:
            raise HTTPException(status_code=404, detail="Toy not found")
        return toy
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching toy: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/toys/{toy_id}", response_model=ToyResponse)
async def update_toy(toy_id: UUID, updates: ToyUpdate):
    """Update toy"""
    logger.info(f"Updating toy: {toy_id}")
    try:
        service = get_toy_service()
        result = service.update(toy_id, updates.model_dump(exclude_unset=True))
        if not result:
            raise HTTPException(status_code=404, detail="Toy not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating toy: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/toys/{toy_id}/activate", response_model=ToyResponse)
async def activate_toy(toy_id: UUID, is_active: bool = True):
    """Activate or deactivate toy"""
    logger.info(f"{'Activating' if is_active else 'Deactivating'} toy: {toy_id}")
    try:
        service = get_toy_service()
        result = service.activate(toy_id, is_active)
        if not result:
            raise HTTPException(status_code=404, detail="Toy not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error activating toy: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/toys/{toy_id}", response_model=BaseResponse)
async def delete_toy(toy_id: UUID):
    """Delete toy (cascades to agents, tools, memories)"""
    logger.info(f"Deleting toy: {toy_id}")
    try:
        service = get_toy_service()
        success = service.delete(toy_id)
        if not success:
            raise HTTPException(status_code=404, detail="Toy not found")
        return BaseResponse(success=True, message="Toy deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting toy: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# AGENT ROUTES
# ============================================================================

@router.post("/agents", response_model=AgentResponse, status_code=201)
async def create_agent(agent: AgentCreate):
    """Create a new agent"""
    logger.info(f"Creating agent: {agent.name} for toy: {agent.toy_id}")
    try:
        service = get_agent_service()
        result = service.create(agent.model_dump())
        return result
    except Exception as e:
        logger.error(f"Error creating agent: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/toys/{toy_id}/agents", response_model=List[AgentResponse])
async def list_agents_by_toy(toy_id: UUID, is_active: Optional[bool] = None):
    """List agents for a toy"""
    logger.info(f"Listing agents for toy: {toy_id}")
    try:
        service = get_agent_service()
        agents = service.list_by_toy(toy_id, is_active)
        return agents
    except Exception as e:
        logger.error(f"Error listing agents: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: UUID, with_providers: bool = False):
    """Get agent by ID"""
    logger.info(f"Fetching agent: {agent_id}")
    try:
        service = get_agent_service()
        if with_providers:
            agent = service.get_with_providers(agent_id)
        else:
            agent = service.get_by_id(agent_id)
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        return agent
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching agent: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/agents/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: UUID, updates: AgentUpdate):
    """Update agent"""
    logger.info(f"Updating agent: {agent_id}")
    try:
        service = get_agent_service()
        result = service.update(agent_id, updates.model_dump(exclude_unset=True))
        if not result:
            raise HTTPException(status_code=404, detail="Agent not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating agent: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/agents/{agent_id}", response_model=BaseResponse)
async def delete_agent(agent_id: UUID):
    """Delete agent (cascades to memories and conversations)"""
    logger.info(f"Deleting agent: {agent_id}")
    try:
        service = get_agent_service()
        success = service.delete(agent_id)
        if not success:
            raise HTTPException(status_code=404, detail="Agent not found")
        return BaseResponse(success=True, message="Agent deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting agent: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# AGENT TOOLS ROUTES
# ============================================================================

@router.post("/tools", response_model=AgentToolResponse, status_code=201)
async def create_agent_tool(tool: AgentToolCreate):
    """Create a new agent tool"""
    logger.info(f"Creating agent tool: {tool.name} for toy: {tool.toy_id}")
    try:
        service = get_agent_tools_service()
        result = service.create(tool.model_dump())
        return result
    except Exception as e:
        logger.error(f"Error creating agent tool: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/toys/{toy_id}/tools", response_model=List[AgentToolResponse])
async def list_tools_by_toy(toy_id: UUID):
    """List tools for a toy"""
    logger.info(f"Listing tools for toy: {toy_id}")
    try:
        service = get_agent_tools_service()
        tools = service.list_by_toy(toy_id)
        return tools
    except Exception as e:
        logger.error(f"Error listing tools: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tools/{tool_id}", response_model=AgentToolResponse)
async def get_tool(tool_id: UUID):
    """Get tool by ID"""
    logger.info(f"Fetching tool: {tool_id}")
    try:
        service = get_agent_tools_service()
        tool = service.get_by_id(tool_id)
        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")
        return tool
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching tool: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/tools/{tool_id}", response_model=AgentToolResponse)
async def update_tool(tool_id: UUID, updates: AgentToolUpdate):
    """Update tool"""
    logger.info(f"Updating tool: {tool_id}")
    try:
        service = get_agent_tools_service()
        result = service.update(tool_id, updates.model_dump(exclude_unset=True))
        if not result:
            raise HTTPException(status_code=404, detail="Tool not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating tool: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/tools/{tool_id}", response_model=BaseResponse)
async def delete_tool(tool_id: UUID):
    """Delete tool"""
    logger.info(f"Deleting tool: {tool_id}")
    try:
        service = get_agent_tools_service()
        success = service.delete(tool_id)
        if not success:
            raise HTTPException(status_code=404, detail="Tool not found")
        return BaseResponse(success=True, message="Tool deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting tool: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
