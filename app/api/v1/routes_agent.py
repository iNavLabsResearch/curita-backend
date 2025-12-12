"""
API routes for Agent CRUD operations
Handles all agent management endpoints
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID

from app.telemetries.logger import logger
from app.data_layer.crud import get_agent_crud
from app.data_layer.data_classes.agent_schemas import (
    AgentCreate,
    AgentUpdate,
    AgentResponse
)

router = APIRouter(prefix="/agents", tags=["Agents"])


# ============================================================================
# CREATE ENDPOINTS
# ============================================================================

@router.post(
    "",
    response_model=AgentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new agent",
    description="Create a new agent for a toy"
)
async def create_agent(agent: AgentCreate):
    """
    Create a new agent
    
    Args:
        agent: Agent creation data
        
    Returns:
        Created agent record
        
    Raises:
        HTTPException 400: Invalid input data
        HTTPException 500: Server error
    """
    logger.info(f"Creating new agent: {agent.name} for toy: {agent.toy_id}")
    
    try:
        crud = get_agent_crud()
        result = await crud.create(agent)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create agent"
            )
        
        logger.info(f"Successfully created agent with ID: {result.id}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating agent: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# READ ENDPOINTS
# ============================================================================

@router.get(
    "/{agent_id}",
    response_model=AgentResponse,
    summary="Get agent by ID",
    description="Retrieve a specific agent by its UUID"
)
async def get_agent(agent_id: UUID):
    """
    Get agent by ID
    
    Args:
        agent_id: UUID of the agent
        
    Returns:
        Agent record
        
    Raises:
        HTTPException 404: Agent not found
        HTTPException 500: Server error
    """
    logger.info(f"Fetching agent with ID: {agent_id}")
    
    try:
        crud = get_agent_crud()
        result = await crud.get_by_id(agent_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with ID {agent_id} not found"
            )
        
        logger.info(f"Successfully retrieved agent: {result.name}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching agent {agent_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "",
    response_model=List[AgentResponse],
    summary="Get all agents",
    description="Retrieve all agents with optional pagination"
)
async def get_all_agents(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    is_active: Optional[bool] = Query(None, description="Filter by active status")
):
    """
    Get all agents with optional filters
    
    Args:
        limit: Maximum number of records
        offset: Number of records to skip
        is_active: Optional filter for active agents only
        
    Returns:
        List of agent records
        
    Raises:
        HTTPException 500: Server error
    """
    logger.info(f"Fetching agents with limit={limit}, offset={offset}, is_active={is_active}")
    
    try:
        crud = get_agent_crud()
        
        if is_active is not None:
            result = await crud.get_all(
                limit=limit,
                offset=offset,
                filters={"is_active": is_active}
            )
        else:
            result = await crud.get_all(limit=limit, offset=offset)
        
        logger.info(f"Successfully retrieved {len(result)} agents")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching agents: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/toy/{toy_id}/all",
    response_model=List[AgentResponse],
    summary="Get agents by toy ID",
    description="Retrieve all agents for a specific toy"
)
async def get_agents_by_toy(toy_id: UUID):
    """
    Get all agents for a toy
    
    Args:
        toy_id: UUID of the toy
        
    Returns:
        List of agent records
        
    Raises:
        HTTPException 500: Server error
    """
    logger.info(f"Fetching agents for toy: {toy_id}")
    
    try:
        crud = get_agent_crud()
        result = await crud.get_by_toy_id(toy_id)
        
        logger.info(f"Successfully retrieved {len(result)} agents for toy {toy_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching agents for toy {toy_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/toy/{toy_id}/active",
    response_model=List[AgentResponse],
    summary="Get active agents by toy ID",
    description="Retrieve all active agents for a specific toy"
)
async def get_active_agents_by_toy(toy_id: UUID):
    """
    Get active agents for a toy
    
    Args:
        toy_id: UUID of the toy
        
    Returns:
        List of active agent records
        
    Raises:
        HTTPException 500: Server error
    """
    logger.info(f"Fetching active agents for toy: {toy_id}")
    
    try:
        crud = get_agent_crud()
        result = await crud.get_active_by_toy_id(toy_id)
        
        logger.info(f"Successfully retrieved {len(result)} active agents for toy {toy_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching active agents for toy {toy_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/provider/model/{provider_id}",
    response_model=List[AgentResponse],
    summary="Get agents by model provider",
    description="Retrieve all agents using a specific model provider"
)
async def get_agents_by_model_provider(provider_id: UUID):
    """
    Get agents by model provider
    
    Args:
        provider_id: UUID of the model provider
        
    Returns:
        List of agent records
        
    Raises:
        HTTPException 500: Server error
    """
    logger.info(f"Fetching agents with model provider: {provider_id}")
    
    try:
        crud = get_agent_crud()
        result = await crud.get_by_model_provider(provider_id)
        
        logger.info(f"Successfully retrieved {len(result)} agents using model provider {provider_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching agents by model provider: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/provider/tts/{provider_id}",
    response_model=List[AgentResponse],
    summary="Get agents by TTS provider",
    description="Retrieve all agents using a specific TTS provider"
)
async def get_agents_by_tts_provider(provider_id: UUID):
    """
    Get agents by TTS provider
    
    Args:
        provider_id: UUID of the TTS provider
        
    Returns:
        List of agent records
        
    Raises:
        HTTPException 500: Server error
    """
    logger.info(f"Fetching agents with TTS provider: {provider_id}")
    
    try:
        crud = get_agent_crud()
        result = await crud.get_by_tts_provider(provider_id)
        
        logger.info(f"Successfully retrieved {len(result)} agents using TTS provider {provider_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching agents by TTS provider: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/provider/transcriber/{provider_id}",
    response_model=List[AgentResponse],
    summary="Get agents by transcriber provider",
    description="Retrieve all agents using a specific transcriber provider"
)
async def get_agents_by_transcriber_provider(provider_id: UUID):
    """
    Get agents by transcriber provider
    
    Args:
        provider_id: UUID of the transcriber provider
        
    Returns:
        List of agent records
        
    Raises:
        HTTPException 500: Server error
    """
    logger.info(f"Fetching agents with transcriber provider: {provider_id}")
    
    try:
        crud = get_agent_crud()
        result = await crud.get_by_transcriber_provider(provider_id)
        
        logger.info(f"Successfully retrieved {len(result)} agents using transcriber provider {provider_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching agents by transcriber provider: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# UPDATE ENDPOINTS
# ============================================================================

@router.put(
    "/{agent_id}",
    response_model=AgentResponse,
    summary="Update agent",
    description="Update an agent's information"
)
async def update_agent(agent_id: UUID, agent: AgentUpdate):
    """
    Update agent
    
    Args:
        agent_id: UUID of the agent to update
        agent: Updated agent data
        
    Returns:
        Updated agent record
        
    Raises:
        HTTPException 404: Agent not found
        HTTPException 500: Server error
    """
    logger.info(f"Updating agent with ID: {agent_id}")
    
    try:
        crud = get_agent_crud()
        result = await crud.update(agent_id, agent)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with ID {agent_id} not found"
            )
        
        logger.info(f"Successfully updated agent: {result.name}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating agent {agent_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# DELETE ENDPOINTS
# ============================================================================

@router.delete(
    "/{agent_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete agent",
    description="Delete an agent by its UUID"
)
async def delete_agent(agent_id: UUID):
    """
    Delete agent
    
    Args:
        agent_id: UUID of the agent to delete
        
    Returns:
        No content
        
    Raises:
        HTTPException 404: Agent not found
        HTTPException 500: Server error
    """
    logger.info(f"Deleting agent with ID: {agent_id}")
    
    try:
        crud = get_agent_crud()
        success = await crud.delete(agent_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with ID {agent_id} not found"
            )
        
        logger.info(f"Successfully deleted agent with ID: {agent_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting agent {agent_id}: {str(e)}", exc_info=True)
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
    summary="Count agents",
    description="Get total count of agents with optional filters"
)
async def count_agents(
    toy_id: Optional[UUID] = Query(None, description="Filter by toy ID"),
    is_active: Optional[bool] = Query(None, description="Filter by active status")
):
    """
    Count agents
    
    Args:
        toy_id: Optional filter by toy ID
        is_active: Optional filter for active agents only
        
    Returns:
        Total count of agents
        
    Raises:
        HTTPException 500: Server error
    """
    logger.info(f"Counting agents with toy_id={toy_id}, is_active={is_active}")
    
    try:
        crud = get_agent_crud()
        
        filters = {}
        if toy_id is not None:
            filters["toy_id"] = toy_id
        if is_active is not None:
            filters["is_active"] = is_active
        
        count = await crud.count(filters=filters if filters else None)
        
        logger.info(f"Total agent count: {count}")
        return count
        
    except Exception as e:
        logger.error(f"Error counting agents: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/exists/{agent_id}",
    response_model=bool,
    summary="Check if agent exists",
    description="Check if an agent with the given ID exists"
)
async def agent_exists(agent_id: UUID):
    """
    Check if agent exists
    
    Args:
        agent_id: UUID of the agent
        
    Returns:
        True if agent exists, False otherwise
        
    Raises:
        HTTPException 500: Server error
    """
    logger.info(f"Checking if agent exists: {agent_id}")
    
    try:
        crud = get_agent_crud()
        exists = await crud.exists(agent_id)
        
        logger.info(f"Agent {agent_id} exists: {exists}")
        return exists
        
    except Exception as e:
        logger.error(f"Error checking agent existence: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
