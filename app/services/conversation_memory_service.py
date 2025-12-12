"""
Conversation Memory Service
Orchestrates the complete text-to-memory pipeline for STT output
"""
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

from app.services.base import BaseDatabaseService
from app.services.text_chunking_service import get_text_chunking_service
from app.services.embedding_service import get_embedding_service
from app.services.conversation_service import get_conversation_service


class ConversationMemoryService(BaseDatabaseService):
    """
    Service for processing STT output and storing in toy_memory + conversation_logs
    
    Pipeline:
    1. Receive extracted text from STT
    2. Chunk text using LangChain
    3. Generate embeddings using Snowflake Arctic XS (384-dim)
    4. Store chunks in toy_memory table with embeddings
    5. Store full text in conversation_logs table
    """
    
    def __init__(self):
        """Initialize conversation memory service"""
        super().__init__(table_name=None)  # Will set toy_memory_table in initialize
        self.chunking_service = None
        self.embedding_service = None
        self.conversation_service = None
        self.toy_memory_table = None
    
    async def initialize(self):
        """Initialize service resources"""
        if self._initialized:
            return
        
        self.logger.info("Initializing conversation memory service")
        
        # Initialize Supabase connection
        await super().initialize()
        
        # Initialize dependent services
        self.chunking_service = get_text_chunking_service()
        self.embedding_service = get_embedding_service()
        self.conversation_service = get_conversation_service()
        self.toy_memory_table = self.settings.TOY_MEMORY_TABLE
        
        self._initialized = True
        self.logger.info("Conversation memory service initialized successfully")
    
    async def process_text_to_memory(
        self,
        text: str,
        toy_id: UUID,
        agent_id: UUID,
        role: str = "user",
        content_type: Optional[str] = "conversation",
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Complete pipeline: Text → Chunks → Embeddings → Storage
        
        Args:
            text: Extracted text from STT
            toy_id: Toy UUID
            agent_id: Agent UUID
            role: Message role (user, assistant, system, tool)
            content_type: Type of content (default: "conversation")
            chunk_size: Optional custom chunk size
            chunk_overlap: Optional custom chunk overlap
            
        Returns:
            Dictionary with:
            - conversation_log_id: UUID of created conversation log
            - toy_memory_ids: List of UUIDs for toy memory chunks
            - chunks_stored: Number of chunks stored
            - total_characters: Total characters processed
        """
        self.logger.info(
            f"Processing text to memory: toy_id={toy_id}, agent_id={agent_id}, "
            f"role={role}, text_length={len(text)}"
        )
        
        await self.initialize()
        
        try:
            # Step 1: Store full text in conversation_logs
            self.logger.debug("Step 1: Storing in conversation_logs")
            conversation_log = await self.conversation_service.add_message(
                agent_id=agent_id,
                role=role,
                content=text
            )
            conversation_log_id = conversation_log["id"]
            self.logger.info(f"Conversation log created: {conversation_log_id}")
            
            # Step 2: Chunk the text
            self.logger.debug("Step 2: Chunking text")
            if chunk_size or chunk_overlap:
                chunking_service = get_text_chunking_service(
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )
            else:
                chunking_service = self.chunking_service
            
            chunks = chunking_service.chunk_text(
                text=text,
                metadata={
                    "source": "stt",
                    "conversation_log_id": str(conversation_log_id),
                    "role": role
                }
            )
            
            if not chunks:
                self.logger.warning("No chunks generated from text")
                return {
                    "conversation_log_id": conversation_log_id,
                    "toy_memory_ids": [],
                    "chunks_stored": 0,
                    "total_characters": len(text)
                }
            
            self.logger.info(f"Text chunked into {len(chunks)} pieces")
            
            # Step 3: Generate embeddings for all chunks
            self.logger.debug("Step 3: Generating embeddings")
            chunk_texts = [chunk["text"] for chunk in chunks]
            embeddings = self.embedding_service.generate_embeddings(chunk_texts)
            self.logger.info(f"Generated {len(embeddings)} embeddings (384-dim)")
            
            # Step 4: Store chunks in toy_memory with embeddings
            self.logger.debug("Step 4: Storing chunks in toy_memory")
            toy_memory_records = []
            
            for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                record = {
                    "toy_id": str(toy_id),
                    "content_type": content_type,
                    "chunk_text": chunk["text"],
                    "embedding_vector": embedding,
                    "chunk_index": idx,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
                toy_memory_records.append(record)
            
            # Batch insert into Supabase
            response = await self.supabase.insert(
                self.toy_memory_table,
                toy_memory_records
            )
            
            toy_memory_ids = [record["id"] for record in response]
            
            self.logger.info(
                f"Successfully stored {len(toy_memory_ids)} chunks in toy_memory"
            )
            
            # Return results
            result = {
                "conversation_log_id": conversation_log_id,
                "toy_memory_ids": toy_memory_ids,
                "chunks_stored": len(toy_memory_ids),
                "total_characters": len(text),
                "chunk_statistics": chunking_service.get_chunk_statistics(chunks)
            }
            
            self.logger.info(
                f"Text-to-memory pipeline completed: {len(toy_memory_ids)} chunks stored"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(
                f"Error in text-to-memory pipeline: {str(e)}",
                exc_info=True
            )
            raise
    
    async def process_batch_texts(
        self,
        texts: List[str],
        toy_id: UUID,
        agent_id: UUID,
        role: str = "user"
    ) -> List[Dict[str, Any]]:
        """
        Process multiple texts in batch
        
        Args:
            texts: List of texts to process
            toy_id: Toy UUID
            agent_id: Agent UUID
            role: Message role
            
        Returns:
            List of results for each text
        """
        self.logger.info(f"Processing batch of {len(texts)} texts")
        
        results = []
        for idx, text in enumerate(texts):
            self.logger.debug(f"Processing text {idx + 1}/{len(texts)}")
            result = await self.process_text_to_memory(
                text=text,
                toy_id=toy_id,
                agent_id=agent_id,
                role=role
            )
            results.append(result)
        
        self.logger.info(f"Batch processing complete: {len(results)} texts processed")
        return results
    
    def get_memory_by_conversation(
        self,
        conversation_log_id: UUID
    ) -> List[Dict[str, Any]]:
        """
        Get all toy_memory chunks associated with a conversation log
        
        Args:
            conversation_log_id: Conversation log UUID
            
        Returns:
            List of memory chunks
        """
        self.logger.info(f"Fetching memory for conversation: {conversation_log_id}")
        
        # Note: This requires metadata to be stored during chunk creation
        # For now, we'll need to query by time range or add a reference field
        
        self.logger.warning(
            "Direct conversation-to-memory lookup not yet implemented. "
            "Consider adding conversation_log_id to toy_memory schema."
        )
        
        return []
    
    async def delete_conversation_memory(
        self,
        conversation_log_id: UUID
    ) -> bool:
        """
        Delete conversation log and associated memory chunks
        
        Args:
            conversation_log_id: Conversation log UUID
            
        Returns:
            True if deleted successfully
        """
        self.logger.info(f"Deleting conversation memory: {conversation_log_id}")
        
        try:
            # Delete conversation log (cascades handled by DB)
            response = self.supabase.table(self.settings.CONVERSATION_LOGS_TABLE)\
                .delete()\
                .eq("id", str(conversation_log_id))\
                .execute()
            
            self.logger.info(f"Conversation log deleted: {conversation_log_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting conversation memory: {str(e)}")
            raise


def get_conversation_memory_service() -> ConversationMemoryService:
    """Get conversation memory service instance"""
    return ConversationMemoryService()
