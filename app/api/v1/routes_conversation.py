"""
API routes for Conversation Log and Message Citation CRUD operations
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
from app.telemetries.logger import logger
from app.data_layer.crud import get_conversation_log_crud, get_message_citation_crud
from app.data_layer.data_classes.conversation_schemas import (
    ConversationLogCreate, ConversationLogResponse,
    MessageCitationCreate, MessageCitationUpdate, MessageCitationResponse
)

# Conversation Log Router
conversation_router = APIRouter(prefix="/conversations", tags=["Conversations"])
# Message Citation Router
citation_router = APIRouter(prefix="/message-citations", tags=["Message Citations"])

# ===== CONVERSATION LOG ROUTES =====
@conversation_router.post("", response_model=ConversationLogResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation_log(log: ConversationLogCreate):
    try:
        crud = get_conversation_log_crud()
        result = await crud.create(log)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create conversation log")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@conversation_router.get("/{log_id}", response_model=ConversationLogResponse)
async def get_conversation_log(log_id: UUID):
    try:
        crud = get_conversation_log_crud()
        result = await crud.get_by_id(log_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Conversation log {log_id} not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@conversation_router.get("", response_model=List[ConversationLogResponse])
async def get_all_conversation_logs(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
    try:
        crud = get_conversation_log_crud()
        return await crud.get_all(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@conversation_router.get("/toy/{toy_id}/history", response_model=List[ConversationLogResponse])
async def get_conversation_history(toy_id: UUID, limit: int = 50):
    try:
        crud = get_conversation_log_crud()
        return await crud.get_conversation_history(toy_id, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@conversation_router.get("/toy/{toy_id}/recent", response_model=List[ConversationLogResponse])
async def get_recent_messages(toy_id: UUID, agent_id: Optional[UUID] = None, limit: int = 20):
    try:
        crud = get_conversation_log_crud()
        return await crud.get_recent_messages(toy_id, agent_id, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@conversation_router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation_log(log_id: UUID):
    try:
        crud = get_conversation_log_crud()
        success = await crud.delete(log_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Conversation log {log_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@conversation_router.get("/count/total", response_model=int)
async def count_conversation_logs(toy_id: Optional[UUID] = Query(None), agent_id: Optional[UUID] = Query(None)):
    try:
        crud = get_conversation_log_crud()
        filters = {}
        if toy_id:
            filters["toy_id"] = toy_id
        if agent_id:
            filters["agent_id"] = agent_id
        return await crud.count(filters=filters if filters else None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== MESSAGE CITATION ROUTES =====
@citation_router.post("", response_model=MessageCitationResponse, status_code=status.HTTP_201_CREATED)
async def create_message_citation(citation: MessageCitationCreate):
    try:
        crud = get_message_citation_crud()
        result = await crud.create(citation)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create message citation")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@citation_router.get("/{citation_id}", response_model=MessageCitationResponse)
async def get_message_citation(citation_id: UUID):
    try:
        crud = get_message_citation_crud()
        result = await crud.get_by_id(citation_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Message citation {citation_id} not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@citation_router.get("", response_model=List[MessageCitationResponse])
async def get_all_message_citations(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
    try:
        crud = get_message_citation_crud()
        return await crud.get_all(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@citation_router.get("/message/{conversation_log_id}/all", response_model=List[MessageCitationResponse])
async def get_citations_for_message(conversation_log_id: UUID):
    try:
        crud = get_message_citation_crud()
        return await crud.get_by_conversation_log(conversation_log_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@citation_router.put("/{citation_id}", response_model=MessageCitationResponse)
async def update_message_citation(citation_id: UUID, citation: MessageCitationUpdate):
    try:
        crud = get_message_citation_crud()
        result = await crud.update(citation_id, citation)
        if not result:
            raise HTTPException(status_code=404, detail=f"Message citation {citation_id} not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@citation_router.delete("/{citation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message_citation(citation_id: UUID):
    try:
        crud = get_message_citation_crud()
        success = await crud.delete(citation_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Message citation {citation_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@citation_router.delete("/message/{conversation_log_id}/all", status_code=status.HTTP_204_NO_CONTENT)
async def delete_citations_for_message(conversation_log_id: UUID):
    try:
        crud = get_message_citation_crud()
        success = await crud.delete_by_conversation_log(conversation_log_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"No citations found for message {conversation_log_id}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@citation_router.get("/count/total", response_model=int)
async def count_message_citations(conversation_log_id: Optional[UUID] = Query(None)):
    try:
        crud = get_message_citation_crud()
        filters = {"conversation_log_id": conversation_log_id} if conversation_log_id else None
        return await crud.count(filters=filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
