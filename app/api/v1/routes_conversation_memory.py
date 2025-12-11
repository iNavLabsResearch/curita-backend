"""
API routes for conversation memory management
Handles text-to-memory pipeline for STT output
"""
from fastapi import APIRouter, HTTPException, status
from typing import List

from app.telemetries.logger import logger
from app.data_layer.data_classes.api_schemas import (
    TextToMemoryRequest,
    TextToMemoryResponse,
    BatchTextToMemoryRequest,
    BatchTextToMemoryResponse,
    BaseResponse,
    SearchMemoryRequest,
    SearchMemoryResponse,
    MemorySearchResult,
)
from app.services.conversation_memory_service import get_conversation_memory_service
from app.services.memory_search_service import get_memory_search_service

router = APIRouter(tags=["Conversation Memory"])


# ============================================================================
# TEXT-TO-MEMORY ENDPOINTS (STT Pipeline)
# ============================================================================

@router.post(
    "/conversation/text-to-memory",
    response_model=TextToMemoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Process extracted text from STT to memory",
    description="""
    Complete pipeline for processing Speech-to-Text output:
    1. Receives extracted text from STT
    2. Chunks text using LangChain RecursiveCharacterTextSplitter
    3. Generates 384-dim embeddings using Snowflake Arctic Embed XS
    4. Stores chunks in toy_memory table with embeddings
    5. Stores full text in conversation_logs table
    
    Returns IDs and statistics for all stored data.
    """
)
async def text_to_memory(request: TextToMemoryRequest):
    """
    Process extracted text from STT and store in memory
    
    Args:
        request: TextToMemoryRequest with text, toy_id, agent_id, etc.
        
    Returns:
        TextToMemoryResponse with conversation_log_id, toy_memory_ids, and statistics
        
    Raises:
        HTTPException 400: Invalid input data
        HTTPException 404: Toy or agent not found
        HTTPException 500: Server error during processing
    """
    logger.info(
        f"Text-to-memory request: toy_id={request.toy_id}, agent_id={request.agent_id}, "
        f"role={request.role}, text_length={len(request.text)}"
    )
    
    try:
        # Validate text is not empty
        if not request.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        
        # Get service and process
        service = get_conversation_memory_service()
        
        result = await service.process_text_to_memory(
            text=request.text,
            toy_id=request.toy_id,
            agent_id=request.agent_id,
            role=request.role,
            content_type=request.content_type,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap
        )
        
        logger.info(
            f"Text-to-memory successful: {result['chunks_stored']} chunks stored, "
            f"conversation_log_id={result['conversation_log_id']}"
        )
        
        return TextToMemoryResponse(
            success=True,
            message=f"Text processed and stored: {result['chunks_stored']} chunks",
            conversation_log_id=result["conversation_log_id"],
            toy_memory_ids=result["toy_memory_ids"],
            chunks_stored=result["chunks_stored"],
            total_characters=result["total_characters"],
            chunk_statistics=result["chunk_statistics"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in text-to-memory pipeline: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process text to memory: {str(e)}"
        )


@router.post(
    "/conversation/batch-text-to-memory",
    response_model=BatchTextToMemoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Process multiple texts in batch",
    description="""
    Batch processing for multiple STT outputs.
    Each text is processed through the complete pipeline independently.
    """
)
async def batch_text_to_memory(request: BatchTextToMemoryRequest):
    """
    Process multiple texts in batch
    
    Args:
        request: BatchTextToMemoryRequest with list of texts
        
    Returns:
        BatchTextToMemoryResponse with results for each text
        
    Raises:
        HTTPException 400: Invalid input data
        HTTPException 500: Server error during processing
    """
    logger.info(
        f"Batch text-to-memory request: {len(request.texts)} texts, "
        f"toy_id={request.toy_id}, agent_id={request.agent_id}"
    )
    
    try:
        service = get_conversation_memory_service()
        
        results = await service.process_batch_texts(
            texts=request.texts,
            toy_id=request.toy_id,
            agent_id=request.agent_id,
            role=request.role
        )
        
        total_chunks = sum(r["chunks_stored"] for r in results)
        
        logger.info(
            f"Batch processing complete: {len(results)} texts, {total_chunks} chunks stored"
        )
        
        return BatchTextToMemoryResponse(
            success=True,
            message=f"Processed {len(results)} texts, {total_chunks} chunks stored",
            results=results,
            total_processed=len(results),
            total_chunks_stored=total_chunks
        )
        
    except Exception as e:
        logger.error(f"Error in batch text-to-memory: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process batch texts: {str(e)}"
        )


@router.post(
    "/conversation/search-memory",
    response_model=SearchMemoryResponse,
    summary="Search memory via Supabase RPC",
    description="Embed query locally then search memory using Supabase RPC functions."
)
async def search_memory(request: SearchMemoryRequest):
    """
    Search memory (toy, agent, or unified) using Supabase RPC functions.
    """
    logger.info(
        f"Search memory request: scope={request.scope}, toy_id={request.toy_id}, "
        f"agent_id={request.agent_id}, match_count={request.match_count}"
    )

    try:
        service = get_memory_search_service()
        results = await service.search_memory(
            query_text=request.query_text,
            match_count=request.match_count,
            similarity_threshold=request.similarity_threshold,
            toy_id=request.toy_id,
            agent_id=request.agent_id,
            scope=request.scope,
        )

        formatted_results = [
            MemorySearchResult(
                id=item.get("id"),
                memory_type=item.get("memory_type") or ("toy" if request.scope == "toy" else "agent"),
                toy_id=item.get("toy_id"),
                agent_id=item.get("agent_id"),
                chunk_text=item.get("chunk_text"),
                chunk_index=item.get("chunk_index"),
                similarity=item.get("similarity"),
                metadata=item.get("metadata"),
                created_at=item.get("created_at"),
            )
            for item in results
        ]

        return SearchMemoryResponse(
            success=True,
            message=f"Found {len(formatted_results)} results",
            results=formatted_results,
            total_results=len(formatted_results),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching memory: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search memory: {str(e)}"
        )


@router.get(
    "/conversation/memory-stats",
    response_model=BaseResponse,
    summary="Get memory statistics",
    description="Get statistics about stored conversation memory"
)
async def get_memory_stats():
    """
    Get statistics about conversation memory storage
    
    Returns:
        Statistics about toy_memory and conversation_logs
    """
    logger.info("Fetching memory statistics")
    
    try:
        # This would require additional service methods
        # For now, return a simple response
        return BaseResponse(
            success=True,
            message="Memory statistics endpoint - implementation pending"
        )
        
    except Exception as e:
        logger.error(f"Error fetching memory stats: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/health",
    response_model=BaseResponse,
    summary="Health check for conversation memory service",
    description="Check if the text-to-memory pipeline is operational"
)
async def health_check():
    """
    Health check endpoint
    
    Returns:
        Health status of the service
    """
    try:
        service = get_conversation_memory_service()
        
        # Basic health check - verify services are initialized
        checks = {
            "chunking_service": service.chunking_service is not None,
            "embedding_service": service.embedding_service is not None,
            "conversation_service": service.conversation_service is not None,
            "supabase": service.supabase is not None
        }
        
        all_healthy = all(checks.values())
        
        return BaseResponse(
            success=all_healthy,
            message="Conversation memory service is healthy" if all_healthy else "Service degraded",
            data={"checks": checks}
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        return BaseResponse(
            success=False,
            message=f"Health check failed: {str(e)}"
        )
