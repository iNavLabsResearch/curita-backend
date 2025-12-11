"""
API routes for RAG search powered by Supabase pgvector RPC.
"""
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.rag_service import get_rag_service
from app.utilities.logger import get_logger

router = APIRouter(prefix="/api/rag", tags=["rag"])
logger = get_logger(__name__)


class RagSearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: Optional[int] = Field(default=None, ge=1, le=100)

    model_config = {"protected_namespaces": ()}


@router.post("/search")
async def search_documents(request: RagSearchRequest):
    """Search similar document chunks using Supabase RPC `match_documents`."""
    try:
        rag_service = get_rag_service()
        results = rag_service.search_similar(request.query, top_k=request.top_k)
        return {"success": True, "query": request.query, "results": results, "count": len(results)}
    except Exception as exc:
        logger.error(f"RAG search failed: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))

