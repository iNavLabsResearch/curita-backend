"""
Text chunking service using LangChain's RecursiveCharacterTextSplitter
Designed for STT (Speech-to-Text) output processing
"""
from typing import List, Dict, Any, Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.services.base import BaseChunkingService


class TextChunkingService(BaseChunkingService):
    """Service for chunking raw text using LangChain"""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        """
        Initialize text chunking service
        
        Args:
            chunk_size: Maximum size of each chunk in characters (default from settings)
            chunk_overlap: Number of characters to overlap between chunks (default from settings)
        """
        super().__init__()
        self.chunk_size = chunk_size or self.settings.DEFAULT_CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or self.settings.DEFAULT_CHUNK_OVERLAP
        self.text_splitter = None
        self._initialize_splitter()
    
    def _initialize_splitter(self):
        """Initialize LangChain text splitter"""
        self.logger.info(
            f"Initializing text chunking service: "
            f"chunk_size={self.chunk_size}, chunk_overlap={self.chunk_overlap}"
        )
        
        # Initialize LangChain's RecursiveCharacterTextSplitter
        # Optimized for conversational text from STT
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            # Separators optimized for conversational text
            separators=["\n\n", "\n", ". ", "! ", "? ", ", ", " ", ""],
            add_start_index=True,
            keep_separator=True
        )
        
        self.logger.info("Text chunking service initialized successfully")
    
    def chunk_text(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Chunk raw text into smaller pieces with metadata
        
        Args:
            text: Raw text to chunk (from STT output)
            metadata: Optional metadata to attach to each chunk
            
        Returns:
            List of chunks with metadata
            [
                {
                    "text": "chunk content",
                    "chunk_index": 0,
                    "start_position": 0,
                    "chunk_size": 150,
                    "metadata": {...}
                },
                ...
            ]
        """
        if not text or not text.strip():
            self.logger.warning("Empty text provided for chunking")
            return []
        
        self.logger.info(f"Chunking text of length {len(text)} characters")
        
        try:
            # Split text using RecursiveCharacterTextSplitter
            chunks = self.text_splitter.split_text(text)
            
            self.logger.debug(f"Text split into {len(chunks)} chunks")
            
            # Format chunks with metadata
            processed_chunks = []
            current_position = 0
            
            for idx, chunk_text in enumerate(chunks):
                chunk_data = {
                    "text": chunk_text,
                    "chunk_index": idx,
                    "start_position": current_position,
                    "chunk_size": len(chunk_text),
                }
                
                # Add custom metadata if provided
                if metadata:
                    chunk_data["metadata"] = metadata
                
                processed_chunks.append(chunk_data)
                
                # Update position for next chunk
                # Account for overlap
                current_position += len(chunk_text) - self.chunk_overlap
            
            self.logger.info(
                f"Successfully chunked text into {len(processed_chunks)} chunks"
            )
            
            return processed_chunks
            
        except Exception as e:
            self.logger.error(f"Error chunking text: {str(e)}", exc_info=True)
            raise
    
    def chunk_with_custom_separators(
        self,
        text: str,
        separators: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Chunk text with custom separators
        
        Args:
            text: Raw text to chunk
            separators: Custom list of separators
            metadata: Optional metadata
            
        Returns:
            List of chunks with metadata
        """
        self.logger.info(f"Chunking with custom separators: {separators}")
        
        # Create a temporary splitter with custom separators
        custom_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=separators,
            add_start_index=True,
            keep_separator=True
        )
        
        chunks = custom_splitter.split_text(text)
        
        # Format chunks
        processed_chunks = []
        current_position = 0
        
        for idx, chunk_text in enumerate(chunks):
            chunk_data = {
                "text": chunk_text,
                "chunk_index": idx,
                "start_position": current_position,
                "chunk_size": len(chunk_text),
            }
            
            if metadata:
                chunk_data["metadata"] = metadata
            
            processed_chunks.append(chunk_data)
            current_position += len(chunk_text) - self.chunk_overlap
        
        return processed_chunks
    
    def get_chunk_statistics(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get statistics about chunks
        
        Args:
            chunks: List of chunks
            
        Returns:
            Statistics dictionary
        """
        if not chunks:
            return {
                "total_chunks": 0,
                "total_characters": 0,
                "avg_chunk_size": 0,
                "min_chunk_size": 0,
                "max_chunk_size": 0
            }
        
        chunk_sizes = [chunk["chunk_size"] for chunk in chunks]
        
        return {
            "total_chunks": len(chunks),
            "total_characters": sum(chunk_sizes),
            "avg_chunk_size": sum(chunk_sizes) / len(chunk_sizes),
            "min_chunk_size": min(chunk_sizes),
            "max_chunk_size": max(chunk_sizes)
        }


def get_text_chunking_service(
    chunk_size: int = None,
    chunk_overlap: int = None
) -> TextChunkingService:
    """
    Get text chunking service instance
    
    Args:
        chunk_size: Optional custom chunk size
        chunk_overlap: Optional custom chunk overlap
        
    Returns:
        TextChunkingService instance
    """
    return TextChunkingService(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
