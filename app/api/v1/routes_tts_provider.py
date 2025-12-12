"""
API routes for TTS Provider CRUD operations
Handles all TTS provider management endpoints
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List
from uuid import UUID

from app.telemetries.logger import logger
from app.data_layer.crud import get_tts_provider_crud
from app.data_layer.data_classes.provider_schemas import (
    TTSProviderCreate,
    TTSProviderUpdate,
    TTSProviderResponse
)

router = APIRouter(prefix="/tts-providers", tags=["TTS Providers"])

@router.post("", response_model=TTSProviderResponse, status_code=status.HTTP_201_CREATED,
    summary="Create a new TTS provider")
async def create_tts_provider(provider: TTSProviderCreate):
    logger.info(f"Creating new TTS provider: {provider.provider_name}/{provider.model_name}")
    try:
        crud = get_tts_provider_crud()
        result = await crud.create(provider)
        if not result:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create TTS provider")
        logger.info(f"Successfully created TTS provider with ID: {result.id}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating TTS provider: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{provider_id}", response_model=TTSProviderResponse,
    summary="Get TTS provider by ID")
async def get_tts_provider(provider_id: UUID):
    logger.info(f"Fetching TTS provider with ID: {provider_id}")
    try:
        crud = get_tts_provider_crud()
        result = await crud.get_by_id(provider_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"TTS provider with ID {provider_id} not found")
        logger.info(f"Successfully retrieved TTS provider: {result.provider_name}/{result.model_name}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching TTS provider {provider_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("", response_model=List[TTSProviderResponse],
    summary="Get all TTS providers")
async def get_all_tts_providers(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)):
    logger.info(f"Fetching TTS providers with limit={limit}, offset={offset}")
    try:
        crud = get_tts_provider_crud()
        result = await crud.get_all(limit=limit, offset=offset)
        logger.info(f"Successfully retrieved {len(result)} TTS providers")
        return result
    except Exception as e:
        logger.error(f"Error fetching TTS providers: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/default/get", response_model=TTSProviderResponse,
    summary="Get default TTS provider")
async def get_default_tts_provider():
    logger.info("Fetching default TTS provider")
    try:
        crud = get_tts_provider_crud()
        result = await crud.get_default()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail="No default TTS provider found")
        logger.info(f"Successfully retrieved default TTS provider: {result.provider_name}/{result.model_name}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching default TTS provider: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/provider/{provider_name}", response_model=List[TTSProviderResponse],
    summary="Get TTS providers by name")
async def get_tts_providers_by_name(provider_name: str, limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
    logger.info(f"Fetching TTS providers for: {provider_name}")
    try:
        crud = get_tts_provider_crud()
        result = await crud.get_by_provider_name(provider_name, limit, offset)
        logger.info(f"Successfully retrieved {len(result)} TTS providers for {provider_name}")
        return result
    except Exception as e:
        logger.error(f"Error fetching TTS providers for {provider_name}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{provider_id}", response_model=TTSProviderResponse,
    summary="Update TTS provider")
async def update_tts_provider(provider_id: UUID, provider: TTSProviderUpdate):
    logger.info(f"Updating TTS provider with ID: {provider_id}")
    try:
        crud = get_tts_provider_crud()
        result = await crud.update(provider_id, provider)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"TTS provider with ID {provider_id} not found")
        logger.info(f"Successfully updated TTS provider: {result.provider_name}/{result.model_name}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating TTS provider {provider_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.patch("/{provider_id}/set-default", response_model=TTSProviderResponse,
    summary="Set default TTS provider")
async def set_default_tts_provider(provider_id: UUID):
    logger.info(f"Setting TTS provider {provider_id} as default")
    try:
        crud = get_tts_provider_crud()
        result = await crud.set_default(provider_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"TTS provider with ID {provider_id} not found")
        logger.info(f"Successfully set default TTS provider: {result.provider_name}/{result.model_name}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error setting default TTS provider: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{provider_id}", status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete TTS provider")
async def delete_tts_provider(provider_id: UUID):
    logger.info(f"Deleting TTS provider with ID: {provider_id}")
    try:
        crud = get_tts_provider_crud()
        success = await crud.delete(provider_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"TTS provider with ID {provider_id} not found")
        logger.info(f"Successfully deleted TTS provider with ID: {provider_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting TTS provider {provider_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/count/total", response_model=int, summary="Count TTS providers")
async def count_tts_providers():
    logger.info("Counting TTS providers")
    try:
        crud = get_tts_provider_crud()
        count = await crud.count()
        logger.info(f"Total TTS provider count: {count}")
        return count
    except Exception as e:
        logger.error(f"Error counting TTS providers: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/exists/{provider_id}", response_model=bool, summary="Check if provider exists")
async def tts_provider_exists(provider_id: UUID):
    logger.info(f"Checking if TTS provider exists: {provider_id}")
    try:
        crud = get_tts_provider_crud()
        exists = await crud.exists(provider_id)
        logger.info(f"TTS provider {provider_id} exists: {exists}")
        return exists
    except Exception as e:
        logger.error(f"Error checking provider existence: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
