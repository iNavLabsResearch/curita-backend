"""
API routes for document upload, search, and CRUD operations
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import Optional
import uuid
import json

from app.core.config import get_settings
from app.utilities.logger import get_logger
from app.models.schemas import (
    SearchRequest,
    SearchByDocumentRequest,
    UpdateChunkRequest,
    DocumentUploadResponse,
    SearchResponse,
    DocumentListResponse,
    DocumentDetailResponse,
    DeleteResponse,
    UpdateChunkResponse,
)
from app.services.document_processor import get_document_processor
from app.services.embedding_service import get_embedding_service
from app.services.vector_storage import get_vector_storage_service
from app.services.search_service import get_search_service


settings = get_settings()
router = APIRouter(prefix="/api/v1", tags=["documents"])
logger = get_logger(__name__)


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    chunk_size: int = Query(None, description="Size of each text chunk"),
    chunk_overlap: int = Query(None, description="Overlap between chunks"),
    metadata: Optional[str] = Query(None, description="Additional metadata as JSON string")
):
    """
    Upload a document, extract text, chunk it, generate embeddings, and store in Supabase
    
    Supported file types: PDF, DOCX, TXT
    """
    logger.info(f"Upload request received: filename={file.filename}, content_type={file.content_type}")
    try:
        # Generate unique document ID
        document_id = str(uuid.uuid4())
        logger.debug(f"Generated document ID: {document_id}")
        
        # Read file content
        file_bytes = await file.read()
        file_type = file.filename.split('.')[-1]
        logger.debug(f"File read successfully: {len(file_bytes)} bytes, type={file_type}")
        
        # Process document using LangChain (extract + chunk in one step)
        logger.info(f"Processing document with chunk_size={chunk_size or settings.DEFAULT_CHUNK_SIZE}, chunk_overlap={chunk_overlap or settings.DEFAULT_CHUNK_OVERLAP}")
        doc_processor = get_document_processor(
            chunk_size=chunk_size or settings.DEFAULT_CHUNK_SIZE,
            chunk_overlap=chunk_overlap or settings.DEFAULT_CHUNK_OVERLAP
        )
        chunks = doc_processor.process_document(file_bytes, file_type, file.filename)
        logger.info(f"Document chunked: {len(chunks)} chunks created")
        
        if not chunks:
            logger.warning(f"No text extracted from document: {file.filename}")
            raise HTTPException(status_code=400, detail="No text could be extracted from the document")
        
        # Generate embeddings for all chunks
        logger.info(f"Generating embeddings for {len(chunks)} chunks")
        embedding_service = get_embedding_service()
        chunk_texts = [chunk["text"] for chunk in chunks]
        embeddings = embedding_service.generate_embeddings(chunk_texts)
        logger.debug(f"Embeddings generated: {len(embeddings)} vectors")
        
        # Prepare metadata
        import json
        doc_metadata = {
            "filename": file.filename,
            "file_type": file_type,
            "total_chunks": len(chunks)
        }
        if metadata:
            try:
                additional_metadata = json.loads(metadata)
                doc_metadata.update(additional_metadata)
                logger.debug(f"Additional metadata added: {additional_metadata}")
            except json.JSONDecodeError:
                logger.warning("Failed to parse additional metadata")
                pass
        
        # Store in Supabase
        logger.info(f"Storing document chunks in vector database: document_id={document_id}")
        vector_storage = get_vector_storage_service()
        stored_chunks = await vector_storage.store_document_chunks(
            document_id=document_id,
            chunks=chunks,
            embeddings=embeddings,
            metadata=doc_metadata
        )
        
        logger.info(f"Document uploaded successfully: document_id={document_id}, filename={file.filename}, chunks={len(stored_chunks)}")
        return DocumentUploadResponse(
            success=True,
            document_id=document_id,
            filename=file.filename,
            total_chunks=len(chunks),
            stored_chunks=len(stored_chunks)
        )
    
    except ValueError as e:
        logger.error(f"Validation error during document upload: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing document {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@router.post("/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """
    Perform semantic search across all documents
    """
    logger.info(f"Search request: query='{request.query[:100]}', top_k={request.top_k}, threshold={request.similarity_threshold}")
    try:
        search_service = get_search_service()
        results = search_service.search(
            query=request.query,
            top_k=request.top_k,
            similarity_threshold=request.similarity_threshold,
            filter_metadata=request.filter_metadata
        )
        
        logger.info(f"Search completed: found {len(results)} results for query '{request.query[:50]}'")
        return SearchResponse(
            success=True,
            query=request.query,
            results=results,
            count=len(results)
        )
    
    except Exception as e:
        logger.error(f"Search error for query '{request.query[:50]}': {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@router.post("/search/document", response_model=SearchResponse)
async def search_by_document(request: SearchByDocumentRequest):
    """
    Search within a specific document
    """
    logger.info(f"Document search request: query='{request.query[:100]}', document_id={request.document_id}, top_k={request.top_k}")
    try:
        search_service = get_search_service()
        results = search_service.search_by_document_id(
            query=request.query,
            document_id=request.document_id,
            top_k=request.top_k
        )
        
        logger.info(f"Document search completed: found {len(results)} results in document {request.document_id}")
        return SearchResponse(
            success=True,
            query=request.query,
            results=results,
            count=len(results)
        )
    
    except Exception as e:
        logger.error(f"Document search error for document {request.document_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@router.get("/documents", response_model=DocumentListResponse)
async def list_documents(
    limit: int = Query(100, description="Maximum number of documents to return"),
    offset: int = Query(0, description="Number of documents to skip")
):
    """
    List all documents with pagination
    """
    logger.info(f"List documents request: limit={limit}, offset={offset}")
    try:
        vector_storage = get_vector_storage_service()
        documents = vector_storage.list_documents(limit=limit, offset=offset)
        logger.debug(f"Retrieved {len(documents)} documents")
        
        logger.info(f"List documents completed: returned {len(documents)} documents")
        return DocumentListResponse(
            success=True,
            documents=documents,
            count=len(documents),
            limit=limit,
            offset=offset
        )
    
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")


@router.get("/documents/{document_id}", response_model=DocumentDetailResponse)
async def get_document(document_id: str):
    """
    Get all chunks for a specific document
    """
    logger.info(f"Get document request: document_id={document_id}")
    try:
        vector_storage = get_vector_storage_service()
        chunks = vector_storage.get_document_chunks(document_id)
        logger.debug(f"Retrieved {len(chunks)} chunks for document {document_id}")
        
        if not chunks:
            logger.warning(f"Document not found: {document_id}")
            raise HTTPException(status_code=404, detail="Document not found")
        
        logger.info(f"Get document completed: document_id={document_id}, total_chunks={len(chunks)}")
        return DocumentDetailResponse(
            success=True,
            document_id=document_id,
            chunks=chunks,
            total_chunks=len(chunks)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving document {document_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error retrieving document: {str(e)}")


@router.delete("/documents/{document_id}", response_model=DeleteResponse)
async def delete_document(document_id: str):
    """
    Delete a document and all its chunks
    """
    logger.info(f"Delete document request: document_id={document_id}")
    try:
        vector_storage = get_vector_storage_service()
        result = vector_storage.delete_document(document_id)
        logger.info(f"Document deleted successfully: document_id={document_id}")
        
        return DeleteResponse(
            success=True,
            message=f"Document {document_id} deleted successfully",
            document_id=document_id
        )
    
    except Exception as e:
        logger.error(f"Error deleting document {document_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")


@router.put("/chunks/{chunk_id}", response_model=UpdateChunkResponse)
async def update_chunk(chunk_id: int, request: UpdateChunkRequest):
    """
    Update a specific chunk
    """
    logger.info(f"Update chunk request: chunk_id={chunk_id}")
    try:
        updates = {}
        
        if request.chunk_text:
            logger.debug(f"Updating chunk text and regenerating embedding for chunk {chunk_id}")
            updates["chunk_text"] = request.chunk_text
            # Regenerate embedding if text changes
            embedding_service = get_embedding_service()
            new_embedding = embedding_service.generate_embedding(request.chunk_text)
            updates["embedding"] = new_embedding
        
        if request.metadata:
            logger.debug(f"Updating metadata for chunk {chunk_id}")
            updates["metadata"] = request.metadata
        
        if not updates:
            logger.warning(f"No updates provided for chunk {chunk_id}")
            raise HTTPException(status_code=400, detail="No updates provided")
        
        vector_storage = get_vector_storage_service()
        updated_chunk = vector_storage.update_chunk(chunk_id, updates)
        
        if not updated_chunk:
            logger.warning(f"Chunk not found: chunk_id={chunk_id}")
            raise HTTPException(status_code=404, detail="Chunk not found")
        
        logger.info(f"Chunk updated successfully: chunk_id={chunk_id}")
        return UpdateChunkResponse(
            success=True,
            message="Chunk updated successfully",
            chunk=updated_chunk
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating chunk {chunk_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error updating chunk: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    logger.debug("Health check requested")
    return {
        "status": "healthy",
        "service": "Curita RAG Backend"
    }
