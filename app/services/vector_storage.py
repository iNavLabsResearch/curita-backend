"""
Vector storage service for Supabase pgvector
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.utilities.supabase_client import get_supabase
from app.services.base import BaseVectorStorage


class SupabaseVectorStorage(BaseVectorStorage):
    """Service for storing and managing vectors in Supabase pgvector"""
    
    def __init__(self, table_name: str = None):
        """
        Initialize vector storage service
        
        Args:
            table_name: Name of the table in Supabase
        """
        super().__init__()
        self.table_name = table_name or self.settings.DOCUMENTS_TABLE
        self.supabase = None
        self.initialize()
    
    def initialize(self):
        """Initialize service resources"""
        self.logger.info("Initializing vector storage service")
        self.supabase = get_supabase()
        self.logger.info(f"Vector storage service initialized with table: {self.table_name}")
    
    async def store_document_chunks(
        self,
        document_id: str,
        chunks: List[Dict[str, Any]],
        embeddings: List[List[float]],
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Store document chunks with their embeddings in Supabase
        
        Args:
            document_id: Unique identifier for the document
            chunks: List of chunk dictionaries with text and metadata
            embeddings: List of embedding vectors corresponding to chunks
            metadata: Optional additional metadata for the document
            
        Returns:
            List of inserted records
        """
        if len(chunks) != len(embeddings):
            error_msg = f"Chunk count ({len(chunks)}) doesn't match embedding count ({len(embeddings)})"
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        
        self.logger.info(f"Storing {len(chunks)} chunks for document {document_id}")
        
        records = []
        for chunk, embedding in zip(chunks, embeddings):
            record = {
                "document_id": document_id,
                "chunk_text": chunk["text"],
                "chunk_index": chunk["chunk_index"],
                "embedding": embedding,
                "metadata": {
                    "start_position": chunk.get("start_position"),
                    "end_position": chunk.get("end_position"),
                    "chunk_size": chunk.get("chunk_size"),
                    **(metadata or {})
                },
                "created_at": datetime.utcnow().isoformat()
            }
            records.append(record)
        
        # Insert into Supabase
        response = self.supabase.table(self.table_name).insert(records).execute()
        
        self.logger.info(f"Successfully stored {len(response.data)} chunks for document {document_id}")
        return response.data
    
    def get_document_chunks(self, document_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all chunks for a specific document
        
        Args:
            document_id: Document identifier
            
        Returns:
            List of document chunks
        """
        self.logger.info(f"Retrieving chunks for document: {document_id}")
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("document_id", document_id)\
            .order("chunk_index")\
            .execute()
        
        self.logger.debug(f"Retrieved {len(response.data)} chunks for document {document_id}")
        return response.data
    
    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """
        Delete all chunks associated with a document
        
        Args:
            document_id: Document identifier
            
        Returns:
            Delete operation result
        """
        self.logger.info(f"Deleting document: {document_id}")
        response = self.supabase.table(self.table_name)\
            .delete()\
            .eq("document_id", document_id)\
            .execute()
        
        self.logger.info(f"Document deleted successfully: {document_id}")
        return {"deleted": True, "document_id": document_id}
    
    def update_chunk(self, chunk_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a specific chunk
        
        Args:
            chunk_id: Chunk identifier
            updates: Dictionary of fields to update
            
        Returns:
            Updated chunk data
        """
        self.logger.info(f"Updating chunk: chunk_id={chunk_id}, fields={list(updates.keys())}")
        response = self.supabase.table(self.table_name)\
            .update(updates)\
            .eq("id", chunk_id)\
            .execute()
        
        self.logger.debug(f"Chunk updated: chunk_id={chunk_id}")
        return response.data[0] if response.data else None
    
    def list_documents(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        List all documents with pagination
        
        Args:
            limit: Maximum number of documents to return
            offset: Number of documents to skip
            
        Returns:
            List of unique documents
        """
        self.logger.info(f"Listing documents: limit={limit}, offset={offset}")
        response = self.supabase.table(self.table_name)\
            .select("document_id, metadata, created_at")\
            .range(offset, offset + limit - 1)\
            .execute()
        
        # Get unique documents
        documents = {}
        for item in response.data:
            doc_id = item["document_id"]
            if doc_id not in documents:
                documents[doc_id] = item
        
        self.logger.debug(f"Found {len(documents)} unique documents")
        return list(documents.values())


def get_vector_storage_service() -> SupabaseVectorStorage:
    """Get vector storage service instance"""
    return SupabaseVectorStorage()
