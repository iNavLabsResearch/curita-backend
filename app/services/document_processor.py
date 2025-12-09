"""
Document processing service for text extraction and chunking using LangChain
"""
from typing import List, Dict, Any, Optional
from io import BytesIO
import tempfile
import os

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredFileLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

from app.services.base import BaseDocumentProcessor


class LangChainDocumentProcessor(BaseDocumentProcessor):
    """Service for extracting text from documents and chunking using LangChain"""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        """
        Initialize document processor
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        super().__init__()
        self.chunk_size = chunk_size or self.settings.DEFAULT_CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or self.settings.DEFAULT_CHUNK_OVERLAP
        self.text_splitter = None
        self.initialize()
    
    def initialize(self):
        """Initialize service resources"""
        # Initialize LangChain's RecursiveCharacterTextSplitter
        self.logger.info(f"Initializing document processor: chunk_size={self.chunk_size}, chunk_overlap={self.chunk_overlap}")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
            add_start_index=True
        )
        self.logger.info("Document processor initialized successfully")
    
    def process_document(self, file_bytes: bytes, file_type: str, filename: str) -> List[Dict[str, Any]]:
        """
        Process document using LangChain loaders and return chunks
        
        Args:
            file_bytes: File content as bytes
            file_type: File extension (pdf, docx, txt)
            filename: Original filename
            
        Returns:
            List of chunks with metadata
        """
        self.logger.info(f"Processing document: {filename} (type: {file_type})")
        
        # Create temporary file for LangChain loaders
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp_file:
            tmp_file.write(file_bytes)
            tmp_file_path = tmp_file.name
        
        try:
            # Load document using appropriate LangChain loader
            file_type = file_type.lower().replace('.', '')
            
            if file_type == 'pdf':
                loader = PyPDFLoader(tmp_file_path)
            elif file_type in ['docx', 'doc']:
                loader = Docx2txtLoader(tmp_file_path)
            elif file_type == 'txt':
                loader = TextLoader(tmp_file_path)
            else:
                # Fallback to unstructured loader for other file types
                self.logger.warning(f"Using fallback loader for file type: {file_type}")
                loader = UnstructuredFileLoader(tmp_file_path)
            
            # Load and split documents
            documents = loader.load()
            self.logger.debug(f"Loaded {len(documents)} document(s) from {filename}")
            
            chunks = self.text_splitter.split_documents(documents)
            self.logger.info(f"Split document into {len(chunks)} chunks")
            
            # Convert LangChain documents to our format
            processed_chunks = []
            for idx, chunk in enumerate(chunks):
                processed_chunks.append({
                    "text": chunk.page_content,
                    "chunk_index": idx,
                    "start_position": chunk.metadata.get("start_index", 0),
                    "chunk_size": len(chunk.page_content),
                    "source_metadata": {
                        "filename": filename,
                        "page": chunk.metadata.get("page", None),
                        "source": chunk.metadata.get("source", filename)
                    }
                })
            
            self.logger.info(f"Successfully processed {filename}: {len(processed_chunks)} chunks created")
            return processed_chunks
        
        except Exception as e:
            self.logger.error(f"Error processing document {filename}: {str(e)}")
            raise
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
                self.logger.debug(f"Cleaned up temporary file: {tmp_file_path}")
    
    def extract_text(self, file_bytes: bytes, file_type: str) -> str:
        """
        Extract text from various file types using LangChain loaders
        
        Args:
            file_bytes: File content as bytes
            file_type: File extension (pdf, docx, txt)
            
        Returns:
            Extracted text
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp_file:
            tmp_file.write(file_bytes)
            tmp_file_path = tmp_file.name
        
        try:
            file_type = file_type.lower().replace('.', '')
            
            if file_type == 'pdf':
                loader = PyPDFLoader(tmp_file_path)
            elif file_type in ['docx', 'doc']:
                loader = Docx2txtLoader(tmp_file_path)
            elif file_type == 'txt':
                loader = TextLoader(tmp_file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            documents = loader.load()
            return "\n".join([doc.page_content for doc in documents])
        
        finally:
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
    
    def chunk_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Chunk text using LangChain's RecursiveCharacterTextSplitter
        
        Args:
            text: Input text to chunk
            metadata: Optional metadata to attach to chunks
            
        Returns:
            List of chunks with metadata
        """
        if not text or not text.strip():
            return []
        
        # Create a Document object
        doc = Document(page_content=text, metadata=metadata or {})
        
        # Split using LangChain text splitter
        chunks = self.text_splitter.split_documents([doc])
        
        # Convert to our format
        processed_chunks = []
        for idx, chunk in enumerate(chunks):
            processed_chunks.append({
                "text": chunk.page_content,
                "chunk_index": idx,
                "start_position": chunk.metadata.get("start_index", 0),
                "chunk_size": len(chunk.page_content),
                "metadata": chunk.metadata
            })
        
        return processed_chunks


def get_document_processor(chunk_size: int = None, chunk_overlap: int = None) -> LangChainDocumentProcessor:
    """Get document processor instance"""
    return LangChainDocumentProcessor(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
