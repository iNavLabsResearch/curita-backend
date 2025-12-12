"""
API routes for Transcriber Provider CRUD operations
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List
from uuid import UUID
from app.telemetries.logger import logger
from app.data_layer.crud import get_transcriber_provider_crud
from app.data_layer.data_classes.provider_schemas import (
    TranscriberProviderCreate, TranscriberProviderUpdate, TranscriberProviderResponse
)

router = APIRouter(prefix="/transcriber-providers", tags=["Transcriber Providers"])

@router.post("", response_model=TranscriberProviderResponse, status_code=status.HTTP_201_CREATED)
async def create_transcriber_provider(provider: TranscriberProviderCreate):
    try:
        crud = get_transcriber_provider_crud()
        result = await crud.create(provider)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create transcriber provider")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{provider_id}", response_model=TranscriberProviderResponse)
async def get_transcriber_provider(provider_id: UUID):
    try:
        crud = get_transcriber_provider_crud()
        result = await crud.get_by_id(provider_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Transcriber provider {provider_id} not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[TranscriberProviderResponse])
async def get_all_transcriber_providers(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
    try:
        crud = get_transcriber_provider_crud()
        return await crud.get_all(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/default/get", response_model=TranscriberProviderResponse)
async def get_default_transcriber_provider():
    try:
        crud = get_transcriber_provider_crud()
        result = await crud.get_default()
        if not result:
            raise HTTPException(status_code=404, detail="No default transcriber provider found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/provider/{provider_name}", response_model=List[TranscriberProviderResponse])
async def get_transcriber_providers_by_name(provider_name: str, limit: int = 100, offset: int = 0):
    try:
        crud = get_transcriber_provider_crud()
        return await crud.get_by_provider_name(provider_name, limit, offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/model-size/{size}", response_model=List[TranscriberProviderResponse])
async def get_transcriber_by_model_size(size: str, limit: int = 100, offset: int = 0):
    try:
        crud = get_transcriber_provider_crud()
        return await crud.get_by_model_size(size, limit, offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{provider_id}", response_model=TranscriberProviderResponse)
async def update_transcriber_provider(provider_id: UUID, provider: TranscriberProviderUpdate):
    try:
        crud = get_transcriber_provider_crud()
        result = await crud.update(provider_id, provider)
        if not result:
            raise HTTPException(status_code=404, detail=f"Transcriber provider {provider_id} not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{provider_id}/set-default", response_model=TranscriberProviderResponse)
async def set_default_transcriber_provider(provider_id: UUID):
    try:
        crud = get_transcriber_provider_crud()
        result = await crud.set_default(provider_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Transcriber provider {provider_id} not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{provider_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transcriber_provider(provider_id: UUID):
    try:
        crud = get_transcriber_provider_crud()
        success = await crud.delete(provider_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Transcriber provider {provider_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/count/total", response_model=int)
async def count_transcriber_providers():
    try:
        crud = get_transcriber_provider_crud()
        return await crud.count()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/exists/{provider_id}", response_model=bool)
async def transcriber_provider_exists(provider_id: UUID):
    try:
        crud = get_transcriber_provider_crud()
        return await crud.exists(provider_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
