"""
Lightweight text extraction and recursive chunking utilities for RAG ingestion.
Uses unstructured for robust extraction and LangChain splitters for chunking.
"""
import os
import tempfile
from typing import Dict, List, Optional

from langchain_text_splitters import RecursiveCharacterTextSplitter
from unstructured.partition.auto import partition

from app.core.config import get_settings
from app.utilities.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


def extract_text_from_file_bytes(file_bytes: bytes, filename: str) -> str:
    """
    Extract raw text from file bytes using unstructured.

    Args:
        file_bytes: Raw bytes of the uploaded file.
        filename: Original filename (used to hint type to unstructured).

    Returns:
        Combined text extracted from the document.
    """
    if not file_bytes:
        return ""

    # Some unstructured loaders expect a file-like object; to maximize
    # compatibility we write to a temporary file that preserves the suffix.
    suffix = f".{filename.split('.')[-1]}" if "." in filename else ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        elements = partition(filename=tmp_path)
        texts = [str(el) for el in elements if str(el).strip()]
        return "\n".join(texts)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def recursive_chunk(
    text: str,
    chunk_size: Optional[int] = None,
    chunk_overlap: Optional[int] = None,
    base_metadata: Optional[Dict] = None,
) -> List[Dict]:
    """
    Chunk text recursively with sensible defaults.

    Args:
        text: The input text to split.
        chunk_size: Optional override for chunk size.
        chunk_overlap: Optional override for overlap.
        base_metadata: Metadata to attach to each chunk.

    Returns:
        List of chunk dictionaries containing text, chunk_index, and metadata.
    """
    if not text or not text.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size or settings.DEFAULT_CHUNK_SIZE,
        chunk_overlap=chunk_overlap or settings.DEFAULT_CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
        add_start_index=True,
    )

    docs = splitter.create_documents([text], metadatas=[base_metadata or {}])
    chunks: List[Dict] = []

    for idx, doc in enumerate(docs):
        chunks.append(
            {
                "text": doc.page_content,
                "chunk_index": idx,
                "metadata": doc.metadata or base_metadata or {},
            }
        )

    return chunks

