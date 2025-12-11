"""
RAG orchestration service:
- ingest documents (extract, chunk, embed, persist to Supabase/pgvector)
- semantic search via Supabase RPC match_documents
"""
import uuid
from typing import Any, Dict, List, Optional

from app.core.config import get_settings
from app.services.base import BaseService
from app.services.embedding_service import embed, embed_batch
from app.services.text_processor import extract_text_from_file_bytes, recursive_chunk
from app.utilities.logger import get_logger
from app.utilities.supabase_client import get_supabase


class RagService(BaseService):
    """High-level RAG operations powered by Supabase pgvector."""

    def __init__(self):
        super().__init__()
        self.supabase = None
        self.initialize()

    def initialize(self):
        """Initialize Supabase client."""
        self.supabase = get_supabase()

    def ingest_document(
        self,
        file_bytes: bytes,
        filename: str,
        source_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Extract text, chunk recursively, embed locally, and store in Supabase.

        Returns a summary containing created document IDs and chunk count.
        """
        logger = get_logger(__name__)
        logger.info(f"Ingesting document: {filename}")

        text = extract_text_from_file_bytes(file_bytes, filename)
        if not text.strip():
            raise ValueError("No text could be extracted from the document")

        chunks = recursive_chunk(
            text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            base_metadata=metadata or {},
        )
        if not chunks:
            raise ValueError("Chunking produced no results")

        embeddings = embed_batch([c["text"] for c in chunks])

        document_rows: List[Dict[str, Any]] = []
        embedding_rows: List[Dict[str, Any]] = []
        for chunk, vector in zip(chunks, embeddings):
            doc_id = str(uuid.uuid4())
            document_rows.append(
                {
                    "id": doc_id,
                    "text": chunk["text"],
                    "chunk_index": chunk.get("chunk_index"),
                    "source_id": source_id,
                    "source_filename": filename,
                    "metadata": chunk.get("metadata") or metadata or {},
                }
            )
            embedding_rows.append(
                {
                    "id": str(uuid.uuid4()),
                    "document_id": doc_id,
                    "embedding": vector,
                }
            )

        # Persist without storing raw file bytes
        doc_resp = self.supabase.table("documents").insert(document_rows).execute()
        if getattr(doc_resp, "error", None):
            raise RuntimeError(f"Failed to insert documents: {doc_resp.error}")

        emb_resp = self.supabase.table("doc_embeddings").insert(embedding_rows).execute()
        if getattr(emb_resp, "error", None):
            raise RuntimeError(f"Failed to insert embeddings: {emb_resp.error}")

        logger.info(f"Ingested {len(document_rows)} chunks for {filename}")
        return {
            "success": True,
            "source_id": source_id,
            "document_ids": [row["id"] for row in document_rows],
            "chunks": len(document_rows),
        }

    def search_similar(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """Embed the query and search Supabase via RPC match_documents."""
        settings = get_settings()
        match_count = top_k or settings.DEFAULT_TOP_K
        query_embedding = embed(query)

        resp = self.supabase.rpc(
            "match_documents",
            {
                "query_embedding": query_embedding,
                "match_count": match_count,
            },
        ).execute()

        if getattr(resp, "error", None):
            raise RuntimeError(f"Supabase RPC match_documents failed: {resp.error}")

        data = getattr(resp, "data", None) or []
        return data


# Singleton accessor
_rag_service: Optional[RagService] = None


def get_rag_service() -> RagService:
    global _rag_service
    if _rag_service is None:
        _rag_service = RagService()
    return _rag_service

