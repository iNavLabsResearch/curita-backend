"""
API routes for RAG document ingestion (upload -> extract -> chunk -> embed -> store).
"""
import json
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.services.rag_service import get_rag_service
from app.utilities.logger import get_logger

router = APIRouter(prefix="/api/documents", tags=["documents"])
logger = get_logger(__name__)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    source_id: Optional[str] = Form(None),
    metadata: Optional[str] = Form(None),
):
    """
    Upload a document and ingest it into Supabase pgvector.

    - Extract text with unstructured
    - Recursive chunking
    - Local embeddings (sentence-transformers)
    - Persist chunks + vectors; raw file is never stored
    """
    try:
        file_bytes = await file.read()
        extra_metadata = {}
        if metadata:
            try:
                extra_metadata = json.loads(metadata)
            except json.JSONDecodeError as exc:
                raise HTTPException(status_code=400, detail=f"Invalid metadata JSON: {exc}") from exc

        rag_service = get_rag_service()
        result = rag_service.ingest_document(
            file_bytes=file_bytes,
            filename=file.filename,
            source_id=source_id,
            metadata=extra_metadata,
        )
        return {"success": True, "filename": file.filename, **result}
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Document upload failed: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))

