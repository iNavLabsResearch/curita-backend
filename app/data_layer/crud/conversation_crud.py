"""
CRUD operations for Conversation entities (Logs and Citations).
Provides database operations for managing conversation history in the system.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from app.data_layer.crud.base_crud import BaseCRUD
from app.data_layer.data_classes.conversation_schemas import (
    ConversationLogCreate,
    ConversationLogResponse,
    MessageCitationCreate,
    MessageCitationResponse,
    MessageWithCitations
)
from app.data_layer.supabase_client import SupabaseClient
from app.telemetries.logger import logger


# ============================================================================
# CONVERSATION LOG CRUD
# ============================================================================

class ConversationLogCRUD(BaseCRUD[ConversationLogCreate, ConversationLogCreate, ConversationLogResponse]):
    """
    CRUD operations for Conversation Log entities.
    
    Handles all database operations related to conversation logs including:
    - Basic CRUD operations (create, read, delete - no update for logs)
    - Queries by agent_id
    - Role-based filtering
    - Conversation history retrieval
    
    Note: Conversation logs are typically immutable (no update operation).
    """
    
    def __init__(self, supabase_client: Optional[SupabaseClient] = None):
        """
        Initialize ConversationLogCRUD instance.
        
        Args:
            supabase_client: Optional Supabase client instance
        """
        super().__init__(
            table_name="conversation_logs",
            response_model=ConversationLogResponse,
            supabase_client=supabase_client
        )
    
    async def get_by_agent_id(
        self,
        agent_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[ConversationLogResponse]:
        """
        Retrieve all conversation logs for a specific agent.
        
        Args:
            agent_id: UUID of the agent
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of conversation log records
        """
        try:
            logger.debug(f"Fetching conversation logs for agent_id: {agent_id}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"agent_id": str(agent_id)},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching conversation logs for agent_id {agent_id}: {str(e)}", exc_info=True)
            return []
    
    async def get_by_role(
        self,
        role: str,
        agent_id: Optional[UUID] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[ConversationLogResponse]:
        """
        Retrieve conversation logs by role.
        
        Args:
            role: Role to filter by ('user', 'assistant', 'system', 'tool')
            agent_id: Optional UUID of agent to filter by
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of conversation log records
        """
        try:
            logger.debug(f"Fetching conversation logs for role: {role}")
            
            filters = {"role": role}
            if agent_id:
                filters["agent_id"] = str(agent_id)
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters=filters,
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching conversation logs for role {role}: {str(e)}", exc_info=True)
            return []
    
    async def get_conversation_history(
        self,
        agent_id: UUID,
        limit: int = 50,
        before: Optional[datetime] = None,
        after: Optional[datetime] = None
    ) -> List[ConversationLogResponse]:
        """
        Retrieve conversation history for an agent with optional time filtering.
        
        Args:
            agent_id: UUID of the agent
            limit: Maximum number of messages to return
            before: Optional datetime to get messages before
            after: Optional datetime to get messages after
            
        Returns:
            List of conversation log records in chronological order
        """
        try:
            logger.debug(f"Fetching conversation history for agent_id: {agent_id}")
            
            # Get logs for the agent
            logs = await self.get_by_agent_id(agent_id, limit=limit * 2, offset=0)
            
            # Filter by time if specified
            if before:
                logs = [log for log in logs if log.created_at < before]
            if after:
                logs = [log for log in logs if log.created_at > after]
            
            # Sort chronologically (oldest first for conversation flow)
            logs.sort(key=lambda x: x.created_at)
            
            # Apply limit
            result = logs[:limit]
            
            logger.info(f"Retrieved {len(result)} conversation logs for agent_id: {agent_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error fetching conversation history for agent_id {agent_id}: {str(e)}", exc_info=True)
            return []
    
    async def get_recent_messages(
        self,
        agent_id: UUID,
        count: int = 10
    ) -> List[ConversationLogResponse]:
        """
        Get the most recent messages for an agent.
        
        Args:
            agent_id: UUID of the agent
            count: Number of recent messages to retrieve
            
        Returns:
            List of recent conversation log records in chronological order
        """
        try:
            logger.debug(f"Fetching {count} recent messages for agent_id: {agent_id}")
            
            logs = await self.get_by_agent_id(agent_id, limit=count, offset=0)
            
            # Reverse to get chronological order (oldest first)
            logs.reverse()
            
            logger.info(f"Retrieved {len(logs)} recent messages for agent_id: {agent_id}")
            return logs
            
        except Exception as e:
            logger.error(f"Error fetching recent messages for agent_id {agent_id}: {str(e)}", exc_info=True)
            return []
    
    async def delete_by_agent_id(self, agent_id: UUID) -> bool:
        """
        Delete all conversation logs for a specific agent.
        
        Args:
            agent_id: UUID of the agent
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            logger.debug(f"Deleting all conversation logs for agent_id: {agent_id}")
            
            result = await self.supabase.delete(
                self.table_name,
                filters={"agent_id": str(agent_id)}
            )
            
            if result:
                logger.info(f"Successfully deleted conversation logs for agent_id: {agent_id}")
                return True
            
            logger.warning(f"Failed to delete conversation logs for agent_id: {agent_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error deleting conversation logs for agent_id {agent_id}: {str(e)}", exc_info=True)
            return False
    
    async def count_by_agent(self, agent_id: UUID) -> int:
        """
        Count total messages for an agent.
        
        Args:
            agent_id: UUID of the agent
            
        Returns:
            Number of conversation logs
        """
        try:
            return await self.count(filters={"agent_id": str(agent_id)})
        except Exception as e:
            logger.error(f"Error counting conversation logs for agent_id {agent_id}: {str(e)}", exc_info=True)
            return 0


# ============================================================================
# MESSAGE CITATION CRUD
# ============================================================================

class MessageCitationCRUD(BaseCRUD[MessageCitationCreate, MessageCitationCreate, MessageCitationResponse]):
    """
    CRUD operations for Message Citation entities.
    
    Handles all database operations related to message citations including:
    - Basic CRUD operations (create, read, delete - no update for citations)
    - Queries by log_id
    - Queries by memory sources
    - Citation retrieval with similarity scores
    
    Note: Message citations are typically immutable (no update operation).
    """
    
    def __init__(self, supabase_client: Optional[SupabaseClient] = None):
        """
        Initialize MessageCitationCRUD instance.
        
        Args:
            supabase_client: Optional Supabase client instance
        """
        super().__init__(
            table_name="message_citations",
            response_model=MessageCitationResponse,
            supabase_client=supabase_client
        )
    
    async def get_by_log_id(
        self,
        log_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[MessageCitationResponse]:
        """
        Retrieve all citations for a specific conversation log.
        
        Args:
            log_id: UUID of the conversation log
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of message citation records sorted by similarity score
        """
        try:
            logger.debug(f"Fetching citations for log_id: {log_id}")
            
            result = await self.supabase.select(
                self.table_name,
                filters={"log_id": str(log_id)},
                limit=limit,
                offset=offset,
                order_by="similarity_score",
                order_desc=True
            )
            
            if result:
                citations = [self.response_model(**record) for record in result]
                logger.info(f"Successfully retrieved {len(citations)} citations for log_id: {log_id}")
                return citations
            
            logger.info(f"No citations found for log_id: {log_id}")
            return []
            
        except Exception as e:
            logger.error(f"Error fetching citations for log_id {log_id}: {str(e)}", exc_info=True)
            return []
    
    async def get_by_toy_memory_id(
        self,
        toy_memory_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[MessageCitationResponse]:
        """
        Retrieve all citations referencing a specific toy memory.
        
        Args:
            toy_memory_id: UUID of the toy memory
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of message citation records
        """
        try:
            logger.debug(f"Fetching citations for toy_memory_id: {toy_memory_id}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"toy_memory_id": str(toy_memory_id)},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching citations for toy_memory_id {toy_memory_id}: {str(e)}", exc_info=True)
            return []
    
    async def get_by_agent_memory_id(
        self,
        agent_memory_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[MessageCitationResponse]:
        """
        Retrieve all citations referencing a specific agent memory.
        
        Args:
            agent_memory_id: UUID of the agent memory
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of message citation records
        """
        try:
            logger.debug(f"Fetching citations for agent_memory_id: {agent_memory_id}")
            
            return await self.get_all(
                limit=limit,
                offset=offset,
                filters={"agent_memory_id": str(agent_memory_id)},
                order_by="created_at",
                order_desc=True
            )
            
        except Exception as e:
            logger.error(f"Error fetching citations for agent_memory_id {agent_memory_id}: {str(e)}", exc_info=True)
            return []
    
    async def get_top_citations(
        self,
        log_id: UUID,
        top_k: int = 5
    ) -> List[MessageCitationResponse]:
        """
        Get the top K citations with highest similarity scores for a message.
        
        Args:
            log_id: UUID of the conversation log
            top_k: Number of top citations to retrieve
            
        Returns:
            List of top message citation records
        """
        try:
            logger.debug(f"Fetching top {top_k} citations for log_id: {log_id}")
            
            citations = await self.get_by_log_id(log_id, limit=top_k, offset=0)
            
            logger.info(f"Retrieved {len(citations)} top citations for log_id: {log_id}")
            return citations
            
        except Exception as e:
            logger.error(f"Error fetching top citations for log_id {log_id}: {str(e)}", exc_info=True)
            return []
    
    async def delete_by_log_id(self, log_id: UUID) -> bool:
        """
        Delete all citations for a specific conversation log.
        
        Args:
            log_id: UUID of the conversation log
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            logger.debug(f"Deleting all citations for log_id: {log_id}")
            
            result = await self.supabase.delete(
                self.table_name,
                filters={"log_id": str(log_id)}
            )
            
            if result:
                logger.info(f"Successfully deleted citations for log_id: {log_id}")
                return True
            
            logger.warning(f"Failed to delete citations for log_id: {log_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error deleting citations for log_id {log_id}: {str(e)}", exc_info=True)
            return False


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def get_message_with_citations(
    log_id: UUID,
    conversation_crud: Optional[ConversationLogCRUD] = None,
    citation_crud: Optional[MessageCitationCRUD] = None
) -> Optional[MessageWithCitations]:
    """
    Retrieve a conversation log with its associated citations.
    
    Args:
        log_id: UUID of the conversation log
        conversation_crud: Optional ConversationLogCRUD instance
        citation_crud: Optional MessageCitationCRUD instance
        
    Returns:
        MessageWithCitations object or None if not found
    """
    try:
        conv_crud = conversation_crud or get_conversation_log_crud()
        cite_crud = citation_crud or get_message_citation_crud()
        
        # Get the conversation log
        log = await conv_crud.get_by_id(log_id)
        if not log:
            logger.warning(f"Conversation log not found: {log_id}")
            return None
        
        # Get citations for this log
        citations = await cite_crud.get_by_log_id(log_id)
        
        return MessageWithCitations(log=log, citations=citations)
        
    except Exception as e:
        logger.error(f"Error getting message with citations for log_id {log_id}: {str(e)}", exc_info=True)
        return None


# ============================================================================
# SINGLETON INSTANCES
# ============================================================================

_conversation_log_crud_instance: Optional[ConversationLogCRUD] = None
_message_citation_crud_instance: Optional[MessageCitationCRUD] = None


def get_conversation_log_crud() -> ConversationLogCRUD:
    """Get or create the singleton ConversationLogCRUD instance."""
    global _conversation_log_crud_instance
    if _conversation_log_crud_instance is None:
        _conversation_log_crud_instance = ConversationLogCRUD()
    return _conversation_log_crud_instance


def get_message_citation_crud() -> MessageCitationCRUD:
    """Get or create the singleton MessageCitationCRUD instance."""
    global _message_citation_crud_instance
    if _message_citation_crud_instance is None:
        _message_citation_crud_instance = MessageCitationCRUD()
    return _message_citation_crud_instance
