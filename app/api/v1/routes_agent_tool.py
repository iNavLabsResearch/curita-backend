"""
API routes for Agent Tool CRUD operations
Handles all agent tool management endpoints
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID

from app.telemetries.logger import logger
from app.data_layer.crud import get_agent_tool_crud
from app.data_layer.data_classes.agent_schemas import (
    AgentToolCreate,
    AgentToolUpdate,
    AgentToolResponse
)

router = APIRouter(prefix="/agent-tools", tags=["Agent Tools"])


# ============================================================================
# CREATE ENDPOINTS
# ============================================================================

@router.post(
    "",
    response_model=AgentToolResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new agent tool",
    description="Create a new tool for agent integration"
)
async def create_agent_tool(tool: AgentToolCreate):
    """Create a new agent tool"""
    logger.info(f"Creating new agent tool: {tool.name} for toy: {tool.toy_id}")
    
    try:
        crud = get_agent_tool_crud()
        result = await crud.create(tool)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create agent tool"
            )
        
        logger.info(f"Successfully created agent tool with ID: {result.id}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating agent tool: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# READ ENDPOINTS
# ============================================================================

@router.get(
    "/{tool_id}",
    response_model=AgentToolResponse,
    summary="Get agent tool by ID",
    description="Retrieve a specific agent tool by its UUID"
)
async def get_agent_tool(tool_id: UUID):
    """Get agent tool by ID"""
    logger.info(f"Fetching agent tool with ID: {tool_id}")
    
    try:
        crud = get_agent_tool_crud()
        result = await crud.get_by_id(tool_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent tool with ID {tool_id} not found"
            )
        
        logger.info(f"Successfully retrieved agent tool: {result.name}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching agent tool {tool_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "",
    response_model=List[AgentToolResponse],
    summary="Get all agent tools",
    description="Retrieve all agent tools with optional pagination"
)
async def get_all_agent_tools(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get all agent tools"""
    logger.info(f"Fetching agent tools with limit={limit}, offset={offset}")
    
    try:
        crud = get_agent_tool_crud()
        result = await crud.get_all(limit=limit, offset=offset)
        
        logger.info(f"Successfully retrieved {len(result)} agent tools")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching agent tools: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/toy/{toy_id}/all",
    response_model=List[AgentToolResponse],
    summary="Get tools by toy ID",
    description="Retrieve all tools for a specific toy"
)
async def get_tools_by_toy(toy_id: UUID):
    """Get all tools for a toy"""
    logger.info(f"Fetching tools for toy: {toy_id}")
    
    try:
        crud = get_agent_tool_crud()
        result = await crud.get_by_toy_id(toy_id)
        
        logger.info(f"Successfully retrieved {len(result)} tools for toy {toy_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching tools for toy {toy_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/provider/{provider_name}",
    response_model=List[AgentToolResponse],
    summary="Get tools by provider",
    description="Retrieve all tools for a specific provider"
)
async def get_tools_by_provider(provider_name: str):
    """Get tools by provider name"""
    logger.info(f"Fetching tools for provider: {provider_name}")
    
    try:
        crud = get_agent_tool_crud()
        result = await crud.get_by_provider_name(provider_name)
        
        logger.info(f"Successfully retrieved {len(result)} tools for provider {provider_name}")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching tools for provider {provider_name}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/http-method/{method}",
    response_model=List[AgentToolResponse],
    summary="Get tools by HTTP method",
    description="Retrieve all tools using a specific HTTP method"
)
async def get_tools_by_http_method(method: str):
    """Get tools by HTTP method"""
    logger.info(f"Fetching tools with HTTP method: {method}")
    
    try:
        crud = get_agent_tool_crud()
        result = await crud.get_by_http_method(method)
        
        logger.info(f"Successfully retrieved {len(result)} tools with method {method}")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching tools by HTTP method: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/search/by-name",
    response_model=List[AgentToolResponse],
    summary="Search tools by name",
    description="Search tools by name pattern within a toy's tools"
)
async def search_tools_by_name(
    name: str = Query(..., min_length=1),
    toy_id: Optional[UUID] = Query(None)
):
    """Search tools by name"""
    logger.info(f"Searching tools with name: {name}, toy_id: {toy_id}")
    
    try:
        crud = get_agent_tool_crud()
        result = await crud.search_by_name(name, toy_id)
        
        logger.info(f"Found {len(result)} tools matching '{name}'")
        return result
        
    except Exception as e:
        logger.error(f"Error searching tools: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# UPDATE ENDPOINTS
# ============================================================================

@router.put(
    "/{tool_id}",
    response_model=AgentToolResponse,
    summary="Update agent tool",
    description="Update an agent tool's information"
)
async def update_agent_tool(tool_id: UUID, tool: AgentToolUpdate):
    """Update agent tool"""
    logger.info(f"Updating agent tool with ID: {tool_id}")
    
    try:
        crud = get_agent_tool_crud()
        result = await crud.update(tool_id, tool)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent tool with ID {tool_id} not found"
            )
        
        logger.info(f"Successfully updated agent tool: {result.name}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating agent tool {tool_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# DELETE ENDPOINTS
# ============================================================================

@router.delete(
    "/{tool_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete agent tool",
    description="Delete an agent tool by its UUID"
)
async def delete_agent_tool(tool_id: UUID):
    """Delete agent tool"""
    logger.info(f"Deleting agent tool with ID: {tool_id}")
    
    try:
        crud = get_agent_tool_crud()
        success = await crud.delete(tool_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent tool with ID {tool_id} not found"
            )
        
        logger.info(f"Successfully deleted agent tool with ID: {tool_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting agent tool {tool_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@router.get(
    "/count/total",
    response_model=int,
    summary="Count agent tools",
    description="Get total count of agent tools with optional filters"
)
async def count_agent_tools(
    toy_id: Optional[UUID] = Query(None),
    provider_name: Optional[str] = Query(None)
):
    """Count agent tools"""
    logger.info(f"Counting tools with toy_id={toy_id}, provider={provider_name}")
    
    try:
        crud = get_agent_tool_crud()
        
        filters = {}
        if toy_id is not None:
            filters["toy_id"] = toy_id
        if provider_name is not None:
            filters["provider_name"] = provider_name
        
        count = await crud.count(filters=filters if filters else None)
        
        logger.info(f"Total agent tool count: {count}")
        return count
        
    except Exception as e:
        logger.error(f"Error counting agent tools: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/exists/{tool_id}",
    response_model=bool,
    summary="Check if tool exists",
    description="Check if an agent tool with the given ID exists"
)
async def tool_exists(tool_id: UUID):
    """Check if agent tool exists"""
    logger.info(f"Checking if agent tool exists: {tool_id}")
    
    try:
        crud = get_agent_tool_crud()
        exists = await crud.exists(tool_id)
        
        logger.info(f"Agent tool {tool_id} exists: {exists}")
        return exists
        
    except Exception as e:
        logger.error(f"Error checking tool existence: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
