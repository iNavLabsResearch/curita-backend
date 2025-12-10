"""
API routes for memory and conversation management
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from uuid import UUID
from typing import List, Optional

from app.telemetries.logger import logger
from app.models.schemas import (
    MemorySearchRequest,
    MemorySearchResponse,
    ConversationLogCreate,
    ConversationLogResponse,
    SendMessageRequest,
    ConversationHistoryResponse,
    MessageWithCitations,
    BaseResponse
)
from app.services.toy_memory_service import get_toy_memory_service
from app.services.agent_memory_service import get_agent_memory_service
from app.services.unified_memory_search import get_unified_memory_search_service
from app.services.conversation_service import get_conversation_service
from app.services.citation_service import get_citation_service
from app.services.document_processor import get_document_processor

router = APIRouter(prefix="/memory")


# ============================================================================
# MEMORY SEARCH
# ============================================================================

@router.post("/memory/search", response_model=MemorySearchResponse)
async def search_memory(request: MemorySearchRequest):
    """Search across toy and/or agent memory"""
    logger.info(f"Memory search: query='{request.query[:50]}...', type={request.memory_type}")
    try:
        service = get_unified_memory_search_service()
        results = service.search(
            query=request.query,
            memory_type=request.memory_type or "both",
            toy_id=request.toy_id,
            agent_id=request.agent_id,
            top_k=request.top_k,
            similarity_threshold=request.similarity_threshold or 0.0
        )
        
        return MemorySearchResponse(
            success=True,
            query=request.query,
            results=results["combined"],
            count=len(results["combined"])
        )
    except Exception as e:
        logger.error(f"Memory search error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# TOY MEMORY
# ============================================================================

@router.post("/toys/{toy_id}/memory", response_model=BaseResponse, status_code=201)
async def upload_to_toy_memory(
    toy_id: UUID,
    file: UploadFile = File(...),
    content_type: Optional[str] = None,
    chunk_size: int = Query(1000, ge=100, le=4000),
    chunk_overlap: int = Query(200, ge=0, le=1000)
):
    """Upload content to toy memory"""
    logger.info(f"Uploading to toy memory: toy={toy_id}, file={file.filename}")
    try:
        # Read and process file
        file_bytes = await file.read()
        file_type = file.filename.split('.')[-1]
        
        doc_processor = get_document_processor(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = doc_processor.process_document(file_bytes, file_type, file.filename)
        
        # Store in toy memory
        service = get_toy_memory_service()
        result = await service.store_chunks(toy_id, chunks, content_type)
        
        return BaseResponse(
            success=True,
            message=f"Stored {len(result)} chunks to toy memory"
        )
    except Exception as e:
        logger.error(f"Error uploading to toy memory: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/toys/{toy_id}/memory")
async def get_toy_memory(toy_id: UUID, limit: int = Query(100, ge=1, le=1000)):
    """Get toy memory chunks"""
    logger.info(f"Fetching toy memory: toy={toy_id}")
    try:
        service = get_toy_memory_service()
        chunks = service.get_by_toy(toy_id, limit)
        return {"success": True, "chunks": chunks, "count": len(chunks)}
    except Exception as e:
        logger.error(f"Error fetching toy memory: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/toys/{toy_id}/memory", response_model=BaseResponse)
async def delete_toy_memory(toy_id: UUID):
    """Delete all toy memory"""
    logger.info(f"Deleting toy memory: {toy_id}")
    try:
        service = get_toy_memory_service()
        service.delete_by_toy(toy_id)
        return BaseResponse(success=True, message="Toy memory deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting toy memory: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# AGENT MEMORY
# ============================================================================

@router.post("/agents/{agent_id}/memory", response_model=BaseResponse, status_code=201)
async def upload_to_agent_memory(
    agent_id: UUID,
    toy_id: UUID,
    file: UploadFile = File(...),
    content_type: Optional[str] = None,
    chunk_size: int = Query(1000, ge=100, le=4000),
    chunk_overlap: int = Query(200, ge=0, le=1000)
):
    """Upload content to agent memory (knowledge base)"""
    logger.info(f"Uploading to agent memory: agent={agent_id}, file={file.filename}")
    try:
        # Read and process file
        file_bytes = await file.read()
        file_type = file.filename.split('.')[-1]
        file_size = len(file_bytes)
        
        doc_processor = get_document_processor(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = doc_processor.process_document(file_bytes, file_type, file.filename)
        
        # Store in agent memory
        service = get_agent_memory_service()
        result = await service.store_chunks(
            toy_id=toy_id,
            agent_id=agent_id,
            chunks=chunks,
            original_filename=file.filename,
            file_size=file_size,
            content_type=content_type or file_type
        )
        
        return BaseResponse(
            success=True,
            message=f"Stored {len(result)} chunks to agent memory"
        )
    except Exception as e:
        logger.error(f"Error uploading to agent memory: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{agent_id}/memory")
async def get_agent_memory(agent_id: UUID, limit: int = Query(100, ge=1, le=1000)):
    """Get agent memory chunks"""
    logger.info(f"Fetching agent memory: agent={agent_id}")
    try:
        service = get_agent_memory_service()
        chunks = service.get_by_agent(agent_id, limit)
        return {"success": True, "chunks": chunks, "count": len(chunks)}
    except Exception as e:
        logger.error(f"Error fetching agent memory: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/agents/{agent_id}/memory", response_model=BaseResponse)
async def delete_agent_memory(agent_id: UUID):
    """Delete all agent memory"""
    logger.info(f"Deleting agent memory: {agent_id}")
    try:
        service = get_agent_memory_service()
        service.delete_by_agent(agent_id)
        return BaseResponse(success=True, message="Agent memory deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting agent memory: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CONVERSATION
# ============================================================================

@router.post("/agents/{agent_id}/conversation", response_model=ConversationLogResponse, status_code=201)
async def add_message(agent_id: UUID, message: ConversationLogCreate):
    """Add a message to conversation"""
    logger.info(f"Adding message to conversation: agent={agent_id}, role={message.role}")
    try:
        service = get_conversation_service()
        result = service.add_message(agent_id, message.role, message.content)
        return result
    except Exception as e:
        logger.error(f"Error adding message: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{agent_id}/conversation")
async def get_conversation_history(
    agent_id: UUID,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    include_citations: bool = False
):
    """Get conversation history for an agent"""
    logger.info(f"Fetching conversation history: agent={agent_id}")
    try:
        conv_service = get_conversation_service()
        messages = conv_service.get_by_agent(agent_id, limit, offset)
        
        if include_citations:
            citation_service = get_citation_service()
            messages_with_citations = []
            for msg in messages:
                citations = citation_service.get_by_log(UUID(msg["id"]))
                messages_with_citations.append({
                    "log": msg,
                    "citations": citations
                })
            return {
                "success": True,
                "agent_id": str(agent_id),
                "messages": messages_with_citations,
                "count": len(messages_with_citations)
            }
        else:
            return {
                "success": True,
                "agent_id": str(agent_id),
                "messages": messages,
                "count": len(messages)
            }
    except Exception as e:
        logger.error(f"Error fetching conversation history: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/agents/{agent_id}/conversation", response_model=BaseResponse)
async def clear_conversation(agent_id: UUID, keep_system: bool = True):
    """Clear conversation history"""
    logger.info(f"Clearing conversation: agent={agent_id}")
    try:
        service = get_conversation_service()
        service.clear_history(agent_id, keep_system)
        return BaseResponse(success=True, message="Conversation cleared successfully")
    except Exception as e:
        logger.error(f"Error clearing conversation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
