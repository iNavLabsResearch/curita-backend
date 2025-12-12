"""
API routes for Toy CRUD operations
Handles all toy management endpoints
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID

from app.telemetries.logger import logger
from app.data_layer.crud import get_toy_crud
from app.data_layer.data_classes.toy_schemas import (
    ToyCreate,
    ToyUpdate,
    ToyResponse
)

router = APIRouter(prefix="/toys", tags=["Toys"])


# ============================================================================
# CREATE ENDPOINTS
# ============================================================================

@router.post(
    "",
    response_model=ToyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new toy",
    description="Create a new toy with the provided data"
)
async def create_toy(toy: ToyCreate):
    """
    Create a new toy
    
    Args:
        toy: Toy creation data
        
    Returns:
        Created toy record
        
    Raises:
        HTTPException 400: Invalid input data
        HTTPException 500: Server error
    """
    logger.info(f"Creating new toy: {toy.name}")
    
    try:
        crud = get_toy_crud()
        result = await crud.create(toy)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create toy"
            )
        
        logger.info(f"Successfully created toy with ID: {result.id}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating toy: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# READ ENDPOINTS
# ============================================================================

@router.get(
    "/{toy_id}",
    response_model=ToyResponse,
    summary="Get toy by ID",
    description="Retrieve a specific toy by its UUID"
)
async def get_toy(toy_id: UUID):
    """
    Get toy by ID
    
    Args:
        toy_id: UUID of the toy
        
    Returns:
        Toy record
        
    Raises:
        HTTPException 404: Toy not found
        HTTPException 500: Server error
    """
    logger.info(f"Fetching toy with ID: {toy_id}")
    
    try:
        crud = get_toy_crud()
        result = await crud.get_by_id(toy_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Toy with ID {toy_id} not found"
            )
        
        logger.info(f"Successfully retrieved toy: {result.name}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching toy {toy_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "",
    response_model=List[ToyResponse],
    summary="Get all toys",
    description="Retrieve all toys with optional pagination"
)
async def get_all_toys(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    is_active: Optional[bool] = Query(None, description="Filter by active status")
):
    """
    Get all toys with optional filters
    
    Args:
        limit: Maximum number of records
        offset: Number of records to skip
        is_active: Optional filter for active toys only
        
    Returns:
        List of toy records
        
    Raises:
        HTTPException 500: Server error
    """
    logger.info(f"Fetching toys with limit={limit}, offset={offset}, is_active={is_active}")
    
    try:
        crud = get_toy_crud()
        
        if is_active is not None:
            result = await crud.get_all(
                limit=limit,
                offset=offset,
                filters={"is_active": is_active}
            )
        else:
            result = await crud.get_all(limit=limit, offset=offset)
        
        logger.info(f"Successfully retrieved {len(result)} toys")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching toys: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/active/list",
    response_model=List[ToyResponse],
    summary="Get active toys",
    description="Retrieve all active toys"
)
async def get_active_toys():
    """
    Get all active toys
    
    Returns:
        List of active toy records
        
    Raises:
        HTTPException 500: Server error
    """
    logger.info("Fetching active toys")
    
    try:
        crud = get_toy_crud()
        result = await crud.get_active_toys()
        
        logger.info(f"Successfully retrieved {len(result)} active toys")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching active toys: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/search/by-name",
    response_model=List[ToyResponse],
    summary="Search toys by name",
    description="Search toys by name pattern (case-insensitive)"
)
async def search_toys_by_name(
    name: str = Query(..., min_length=1, description="Name pattern to search for")
):
    """
    Search toys by name
    
    Args:
        name: Name pattern to search for
        
    Returns:
        List of matching toy records
        
    Raises:
        HTTPException 500: Server error
    """
    logger.info(f"Searching toys with name pattern: {name}")
    
    try:
        crud = get_toy_crud()
        result = await crud.search_by_name(name)
        
        logger.info(f"Found {len(result)} toys matching '{name}'")
        return result
        
    except Exception as e:
        logger.error(f"Error searching toys: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# UPDATE ENDPOINTS
# ============================================================================

@router.put(
    "/{toy_id}",
    response_model=ToyResponse,
    summary="Update toy",
    description="Update a toy's information"
)
async def update_toy(toy_id: UUID, toy: ToyUpdate):
    """
    Update toy
    
    Args:
        toy_id: UUID of the toy to update
        toy: Updated toy data
        
    Returns:
        Updated toy record
        
    Raises:
        HTTPException 404: Toy not found
        HTTPException 500: Server error
    """
    logger.info(f"Updating toy with ID: {toy_id}")
    
    try:
        crud = get_toy_crud()
        result = await crud.update(toy_id, toy)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Toy with ID {toy_id} not found"
            )
        
        logger.info(f"Successfully updated toy: {result.name}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating toy {toy_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.patch(
    "/{toy_id}/activate",
    response_model=ToyResponse,
    summary="Activate toy",
    description="Set a toy's is_active flag to true"
)
async def activate_toy(toy_id: UUID):
    """
    Activate toy
    
    Args:
        toy_id: UUID of the toy to activate
        
    Returns:
        Updated toy record
        
    Raises:
        HTTPException 404: Toy not found
        HTTPException 500: Server error
    """
    logger.info(f"Activating toy with ID: {toy_id}")
    
    try:
        crud = get_toy_crud()
        result = await crud.activate(toy_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Toy with ID {toy_id} not found"
            )
        
        logger.info(f"Successfully activated toy: {result.name}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error activating toy {toy_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.patch(
    "/{toy_id}/deactivate",
    response_model=ToyResponse,
    summary="Deactivate toy",
    description="Set a toy's is_active flag to false"
)
async def deactivate_toy(toy_id: UUID):
    """
    Deactivate toy
    
    Args:
        toy_id: UUID of the toy to deactivate
        
    Returns:
        Updated toy record
        
    Raises:
        HTTPException 404: Toy not found
        HTTPException 500: Server error
    """
    logger.info(f"Deactivating toy with ID: {toy_id}")
    
    try:
        crud = get_toy_crud()
        result = await crud.deactivate(toy_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Toy with ID {toy_id} not found"
            )
        
        logger.info(f"Successfully deactivated toy: {result.name}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deactivating toy {toy_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# DELETE ENDPOINTS
# ============================================================================

@router.delete(
    "/{toy_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete toy",
    description="Delete a toy by its UUID"
)
async def delete_toy(toy_id: UUID):
    """
    Delete toy
    
    Args:
        toy_id: UUID of the toy to delete
        
    Returns:
        No content
        
    Raises:
        HTTPException 404: Toy not found
        HTTPException 500: Server error
    """
    logger.info(f"Deleting toy with ID: {toy_id}")
    
    try:
        crud = get_toy_crud()
        success = await crud.delete(toy_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Toy with ID {toy_id} not found"
            )
        
        logger.info(f"Successfully deleted toy with ID: {toy_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting toy {toy_id}: {str(e)}", exc_info=True)
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
    summary="Count toys",
    description="Get total count of toys with optional filters"
)
async def count_toys(
    is_active: Optional[bool] = Query(None, description="Filter by active status")
):
    """
    Count toys
    
    Args:
        is_active: Optional filter for active toys only
        
    Returns:
        Total count of toys
        
    Raises:
        HTTPException 500: Server error
    """
    logger.info(f"Counting toys with is_active={is_active}")
    
    try:
        crud = get_toy_crud()
        
        if is_active is not None:
            count = await crud.count(filters={"is_active": is_active})
        else:
            count = await crud.count()
        
        logger.info(f"Total toy count: {count}")
        return count
        
    except Exception as e:
        logger.error(f"Error counting toys: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/exists/{toy_id}",
    response_model=bool,
    summary="Check if toy exists",
    description="Check if a toy with the given ID exists"
)
async def toy_exists(toy_id: UUID):
    """
    Check if toy exists
    
    Args:
        toy_id: UUID of the toy
        
    Returns:
        True if toy exists, False otherwise
        
    Raises:
        HTTPException 500: Server error
    """
    logger.info(f"Checking if toy exists: {toy_id}")
    
    try:
        crud = get_toy_crud()
        exists = await crud.exists(toy_id)
        
        logger.info(f"Toy {toy_id} exists: {exists}")
        return exists
        
    except Exception as e:
        logger.error(f"Error checking toy existence: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
