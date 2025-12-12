"""
API routes for Model Provider CRUD operations
Handles all model provider management endpoints
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID

from app.telemetries.logger import logger
from app.data_layer.crud import get_model_provider_crud
from app.data_layer.data_classes.provider_schemas import (
    ModelProviderCreate,
    ModelProviderUpdate,
    ModelProviderResponse
)

router = APIRouter(prefix="/model-providers", tags=["Model Providers"])


# ============================================================================
# CREATE ENDPOINTS
# ============================================================================

@router.post(
    "",
    response_model=ModelProviderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new model provider",
    description="Create a new model provider configuration"
)
async def create_model_provider(provider: ModelProviderCreate):
    """Create a new model provider"""
    logger.info(f"Creating new model provider: {provider.provider_name}/{provider.model_name}")
    
    try:
        crud = get_model_provider_crud()
        result = await crud.create(provider)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create model provider"
            )
        
        logger.info(f"Successfully created model provider with ID: {result.id}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating model provider: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# READ ENDPOINTS
# ============================================================================

@router.get(
    "/{provider_id}",
    response_model=ModelProviderResponse,
    summary="Get model provider by ID",
    description="Retrieve a specific model provider by its UUID"
)
async def get_model_provider(provider_id: UUID):
    """Get model provider by ID"""
    logger.info(f"Fetching model provider with ID: {provider_id}")
    
    try:
        crud = get_model_provider_crud()
        result = await crud.get_by_id(provider_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model provider with ID {provider_id} not found"
            )
        
        logger.info(f"Successfully retrieved model provider: {result.provider_name}/{result.model_name}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching model provider {provider_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "",
    response_model=List[ModelProviderResponse],
    summary="Get all model providers",
    description="Retrieve all model providers with optional pagination"
)
async def get_all_model_providers(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get all model providers"""
    logger.info(f"Fetching model providers with limit={limit}, offset={offset}")
    
    try:
        crud = get_model_provider_crud()
        result = await crud.get_all(limit=limit, offset=offset)
        
        logger.info(f"Successfully retrieved {len(result)} model providers")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching model providers: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/default/get",
    response_model=ModelProviderResponse,
    summary="Get default model provider",
    description="Retrieve the default model provider"
)
async def get_default_model_provider():
    """Get default model provider"""
    logger.info("Fetching default model provider")
    
    try:
        crud = get_model_provider_crud()
        result = await crud.get_default()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No default model provider found"
            )
        
        logger.info(f"Successfully retrieved default model provider: {result.provider_name}/{result.model_name}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching default model provider: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/provider/{provider_name}",
    response_model=List[ModelProviderResponse],
    summary="Get model providers by name",
    description="Retrieve all model providers for a specific provider name"
)
async def get_model_providers_by_name(
    provider_name: str,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get model providers by provider name"""
    logger.info(f"Fetching model providers for: {provider_name}")
    
    try:
        crud = get_model_provider_crud()
        result = await crud.get_by_provider_name(provider_name, limit, offset)
        
        logger.info(f"Successfully retrieved {len(result)} model providers for {provider_name}")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching model providers for {provider_name}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/large-models/list",
    response_model=List[ModelProviderResponse],
    summary="Get large model providers",
    description="Retrieve all large model providers"
)
async def get_large_model_providers(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get large model providers"""
    logger.info("Fetching large model providers")
    
    try:
        crud = get_model_provider_crud()
        result = await crud.get_large_models(limit, offset)
        
        logger.info(f"Successfully retrieved {len(result)} large model providers")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching large model providers: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# UPDATE ENDPOINTS
# ============================================================================

@router.put(
    "/{provider_id}",
    response_model=ModelProviderResponse,
    summary="Update model provider",
    description="Update a model provider's information"
)
async def update_model_provider(provider_id: UUID, provider: ModelProviderUpdate):
    """Update model provider"""
    logger.info(f"Updating model provider with ID: {provider_id}")
    
    try:
        crud = get_model_provider_crud()
        result = await crud.update(provider_id, provider)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model provider with ID {provider_id} not found"
            )
        
        logger.info(f"Successfully updated model provider: {result.provider_name}/{result.model_name}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating model provider {provider_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.patch(
    "/{provider_id}/set-default",
    response_model=ModelProviderResponse,
    summary="Set default model provider",
    description="Set a model provider as the default (unsets previous default)"
)
async def set_default_model_provider(provider_id: UUID):
    """Set default model provider"""
    logger.info(f"Setting model provider {provider_id} as default")
    
    try:
        crud = get_model_provider_crud()
        result = await crud.set_default(provider_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model provider with ID {provider_id} not found"
            )
        
        logger.info(f"Successfully set default model provider: {result.provider_name}/{result.model_name}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error setting default model provider: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# DELETE ENDPOINTS
# ============================================================================

@router.delete(
    "/{provider_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete model provider",
    description="Delete a model provider by its UUID"
)
async def delete_model_provider(provider_id: UUID):
    """Delete model provider"""
    logger.info(f"Deleting model provider with ID: {provider_id}")
    
    try:
        crud = get_model_provider_crud()
        success = await crud.delete(provider_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model provider with ID {provider_id} not found"
            )
        
        logger.info(f"Successfully deleted model provider with ID: {provider_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting model provider {provider_id}: {str(e)}", exc_info=True)
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
    summary="Count model providers",
    description="Get total count of model providers"
)
async def count_model_providers(
    is_large_model: Optional[bool] = Query(None)
):
    """Count model providers"""
    logger.info(f"Counting model providers with is_large_model={is_large_model}")
    
    try:
        crud = get_model_provider_crud()
        
        filters = {}
        if is_large_model is not None:
            filters["is_large_model"] = is_large_model
        
        count = await crud.count(filters=filters if filters else None)
        
        logger.info(f"Total model provider count: {count}")
        return count
        
    except Exception as e:
        logger.error(f"Error counting model providers: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/exists/{provider_id}",
    response_model=bool,
    summary="Check if provider exists",
    description="Check if a model provider with the given ID exists"
)
async def model_provider_exists(provider_id: UUID):
    """Check if model provider exists"""
    logger.info(f"Checking if model provider exists: {provider_id}")
    
    try:
        crud = get_model_provider_crud()
        exists = await crud.exists(provider_id)
        
        logger.info(f"Model provider {provider_id} exists: {exists}")
        return exists
        
    except Exception as e:
        logger.error(f"Error checking provider existence: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
