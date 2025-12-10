"""
API routes for provider management
"""
from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from typing import List

from app.utilities.logger import get_logger
from app.models.schemas import (
    ModelProviderCreate,
    ModelProviderUpdate,
    ModelProviderResponse,
    TTSProviderCreate,
    TTSProviderUpdate,
    TTSProviderResponse,
    TranscriberProviderCreate,
    TranscriberProviderUpdate,
    TranscriberProviderResponse,
    BaseResponse,
)
from app.services.provider_service import (
    get_model_provider_service,
    get_tts_provider_service,
    get_transcriber_provider_service
)

router = APIRouter(prefix="/api/v1/providers", tags=["providers"])
logger = get_logger(__name__)


# ============================================================================
# MODEL PROVIDERS
# ============================================================================

@router.post("/models", response_model=ModelProviderResponse, status_code=201)
async def create_model_provider(provider: ModelProviderCreate):
    """Create a new model provider"""
    logger.info(f"Creating model provider: {provider.provider_name}")
    try:
        service = get_model_provider_service()
        result = service.create(provider.model_dump())
        return result
    except Exception as e:
        logger.error(f"Error creating model provider: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models", response_model=List[ModelProviderResponse])
async def list_model_providers(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """List all model providers"""
    logger.info(f"Listing model providers: limit={limit}, offset={offset}")
    try:
        service = get_model_provider_service()
        providers = service.list(limit=limit, offset=offset)
        return providers
    except Exception as e:
        logger.error(f"Error listing model providers: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/default", response_model=ModelProviderResponse)
async def get_default_model_provider():
    """Get the default model provider"""
    logger.info("Fetching default model provider")
    try:
        service = get_model_provider_service()
        provider = service.get_default()
        if not provider:
            raise HTTPException(status_code=404, detail="No default model provider found")
        return provider
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching default model provider: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/{provider_id}", response_model=ModelProviderResponse)
async def get_model_provider(provider_id: UUID):
    """Get model provider by ID"""
    logger.info(f"Fetching model provider: {provider_id}")
    try:
        service = get_model_provider_service()
        provider = service.get_by_id(provider_id)
        if not provider:
            raise HTTPException(status_code=404, detail="Model provider not found")
        return provider
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching model provider: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/models/{provider_id}", response_model=ModelProviderResponse)
async def update_model_provider(provider_id: UUID, updates: ModelProviderUpdate):
    """Update model provider"""
    logger.info(f"Updating model provider: {provider_id}")
    try:
        service = get_model_provider_service()
        result = service.update(provider_id, updates.model_dump(exclude_unset=True))
        if not result:
            raise HTTPException(status_code=404, detail="Model provider not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating model provider: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/models/{provider_id}/set-default", response_model=ModelProviderResponse)
async def set_default_model_provider(provider_id: UUID):
    """Set a model provider as default"""
    logger.info(f"Setting model provider as default: {provider_id}")
    try:
        service = get_model_provider_service()
        result = service.set_default(provider_id)
        if not result:
            raise HTTPException(status_code=404, detail="Model provider not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error setting default model provider: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/models/{provider_id}", response_model=BaseResponse)
async def delete_model_provider(provider_id: UUID):
    """Delete model provider"""
    logger.info(f"Deleting model provider: {provider_id}")
    try:
        service = get_model_provider_service()
        success = service.delete(provider_id)
        if not success:
            raise HTTPException(status_code=404, detail="Model provider not found")
        return BaseResponse(success=True, message="Model provider deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting model provider: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# TTS PROVIDERS
# ============================================================================

@router.post("/tts", response_model=TTSProviderResponse, status_code=201)
async def create_tts_provider(provider: TTSProviderCreate):
    """Create a new TTS provider"""
    logger.info(f"Creating TTS provider: {provider.provider_name}")
    try:
        service = get_tts_provider_service()
        result = service.create(provider.model_dump())
        return result
    except Exception as e:
        logger.error(f"Error creating TTS provider: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tts", response_model=List[TTSProviderResponse])
async def list_tts_providers(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """List all TTS providers"""
    logger.info(f"Listing TTS providers: limit={limit}, offset={offset}")
    try:
        service = get_tts_provider_service()
        providers = service.list(limit=limit, offset=offset)
        return providers
    except Exception as e:
        logger.error(f"Error listing TTS providers: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tts/{provider_id}", response_model=TTSProviderResponse)
async def get_tts_provider(provider_id: UUID):
    """Get TTS provider by ID"""
    logger.info(f"Fetching TTS provider: {provider_id}")
    try:
        service = get_tts_provider_service()
        provider = service.get_by_id(provider_id)
        if not provider:
            raise HTTPException(status_code=404, detail="TTS provider not found")
        return provider
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching TTS provider: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/tts/{provider_id}", response_model=TTSProviderResponse)
async def update_tts_provider(provider_id: UUID, updates: TTSProviderUpdate):
    """Update TTS provider"""
    logger.info(f"Updating TTS provider: {provider_id}")
    try:
        service = get_tts_provider_service()
        result = service.update(provider_id, updates.model_dump(exclude_unset=True))
        if not result:
            raise HTTPException(status_code=404, detail="TTS provider not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating TTS provider: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/tts/{provider_id}", response_model=BaseResponse)
async def delete_tts_provider(provider_id: UUID):
    """Delete TTS provider"""
    logger.info(f"Deleting TTS provider: {provider_id}")
    try:
        service = get_tts_provider_service()
        success = service.delete(provider_id)
        if not success:
            raise HTTPException(status_code=404, detail="TTS provider not found")
        return BaseResponse(success=True, message="TTS provider deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting TTS provider: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# TRANSCRIBER PROVIDERS
# ============================================================================

@router.post("/transcribers", response_model=TranscriberProviderResponse, status_code=201)
async def create_transcriber_provider(provider: TranscriberProviderCreate):
    """Create a new transcriber provider"""
    logger.info(f"Creating transcriber provider: {provider.provider_name}")
    try:
        service = get_transcriber_provider_service()
        result = service.create(provider.model_dump())
        return result
    except Exception as e:
        logger.error(f"Error creating transcriber provider: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/transcribers", response_model=List[TranscriberProviderResponse])
async def list_transcriber_providers(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """List all transcriber providers"""
    logger.info(f"Listing transcriber providers: limit={limit}, offset={offset}")
    try:
        service = get_transcriber_provider_service()
        providers = service.list(limit=limit, offset=offset)
        return providers
    except Exception as e:
        logger.error(f"Error listing transcriber providers: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/transcribers/{provider_id}", response_model=TranscriberProviderResponse)
async def get_transcriber_provider(provider_id: UUID):
    """Get transcriber provider by ID"""
    logger.info(f"Fetching transcriber provider: {provider_id}")
    try:
        service = get_transcriber_provider_service()
        provider = service.get_by_id(provider_id)
        if not provider:
            raise HTTPException(status_code=404, detail="Transcriber provider not found")
        return provider
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching transcriber provider: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/transcribers/{provider_id}", response_model=TranscriberProviderResponse)
async def update_transcriber_provider(provider_id: UUID, updates: TranscriberProviderUpdate):
    """Update transcriber provider"""
    logger.info(f"Updating transcriber provider: {provider_id}")
    try:
        service = get_transcriber_provider_service()
        result = service.update(provider_id, updates.model_dump(exclude_unset=True))
        if not result:
            raise HTTPException(status_code=404, detail="Transcriber provider not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating transcriber provider: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/transcribers/{provider_id}", response_model=BaseResponse)
async def delete_transcriber_provider(provider_id: UUID):
    """Delete transcriber provider"""
    logger.info(f"Deleting transcriber provider: {provider_id}")
    try:
        service = get_transcriber_provider_service()
        success = service.delete(provider_id)
        if not success:
            raise HTTPException(status_code=404, detail="Transcriber provider not found")
        return BaseResponse(success=True, message="Transcriber provider deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting transcriber provider: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
