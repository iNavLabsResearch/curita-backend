"""
CRUD operations for Conversations (Conversation Logs and Message Citations)
"""
from uuid import UUID
from typing import List, Optional
from app.data_layer.supabase_client import SupabaseClient
from app.data_layer.crud.base_crud import BaseCrud
from app.data_layer.data_classes.conversation_schemas import (
    ConversationLogResponse,
    MessageCitationResponse,
    MessageWithCitations,
)
from app.telemetries.logger import logger


class ConversationLogCRUD(BaseCrud):
    """CRUD operations for conversation_logs table"""
    
    def __init__(self, supabase: SupabaseClient):
        super().__init__(supabase, "conversation_logs", ConversationLogResponse)
    
    async def get_logs_by_agent(self, agent_id: UUID) -> List[ConversationLogResponse]:
        """
        Get all conversation logs for a specific agent
        
        Args:
            agent_id: UUID of the agent
            
        Returns:
            List of conversation log records
        """
        try:
            logger.debug(f"Fetching conversation logs for agent {agent_id}")
            return await self.filter_by(agent_id=str(agent_id))
        except Exception as e:
            logger.error(f"Error fetching conversation logs for agent {agent_id}: {str(e)}")
            raise
    
    async def get_logs_by_role(self, agent_id: UUID, role: str) -> List[ConversationLogResponse]:
        """
        Get conversation logs by role for a specific agent
        
        Args:
            agent_id: UUID of the agent
            role: Role of the message (user, assistant, system, tool)
            
        Returns:
            List of conversation log records
        """
        try:
            logger.debug(f"Fetching conversation logs for agent {agent_id} with role {role}")
            return await self.filter_by(agent_id=str(agent_id), role=role)
        except Exception as e:
            logger.error(f"Error fetching conversation logs by role: {str(e)}")
            raise
    
    async def get_recent_logs(self, agent_id: UUID, limit: int = 50) -> List[ConversationLogResponse]:
        """
        Get recent conversation logs for a specific agent
        
        Args:
            agent_id: UUID of the agent
            limit: Maximum number of logs to return
            
        Returns:
            List of conversation log records ordered by created_at descending
        """
        try:
            logger.debug(f"Fetching recent conversation logs for agent {agent_id}")
            response = await self.supabase.table(self.table_name).select("*").eq("agent_id", str(agent_id)).order("created_at", desc=True).limit(limit).execute()
            items = []
            for item in response.data:
                items.append(self.model_class(**item))
            return items
        except Exception as e:
            logger.error(f"Error fetching recent conversation logs: {str(e)}")
            raise


class MessageCitationCRUD(BaseCrud):
    """CRUD operations for message_citations table"""
    
    def __init__(self, supabase: SupabaseClient):
        super().__init__(supabase, "message_citations", MessageCitationResponse)
    
    async def get_citations_by_log(self, log_id: UUID) -> List[MessageCitationResponse]:
        """
        Get all citations for a specific conversation log
        
        Args:
            log_id: UUID of the conversation log
            
        Returns:
            List of message citation records
        """
        try:
            logger.debug(f"Fetching citations for log {log_id}")
            return await self.filter_by(log_id=str(log_id))
        except Exception as e:
            logger.error(f"Error fetching citations for log {log_id}: {str(e)}")
            raise
    
    async def get_citations_by_toy_memory(self, toy_memory_id: UUID) -> List[MessageCitationResponse]:
        """
        Get all citations referencing a specific toy memory
        
        Args:
            toy_memory_id: UUID of the toy memory
            
        Returns:
            List of message citation records
        """
        try:
            logger.debug(f"Fetching citations for toy memory {toy_memory_id}")
            return await self.filter_by(toy_memory_id=str(toy_memory_id))
        except Exception as e:
            logger.error(f"Error fetching citations by toy memory: {str(e)}")
            raise
    
    async def get_citations_by_agent_memory(self, agent_memory_id: UUID) -> List[MessageCitationResponse]:
        """
        Get all citations referencing a specific agent memory
        
        Args:
            agent_memory_id: UUID of the agent memory
            
        Returns:
            List of message citation records
        """
        try:
            logger.debug(f"Fetching citations for agent memory {agent_memory_id}")
            return await self.filter_by(agent_memory_id=str(agent_memory_id))
        except Exception as e:
            logger.error(f"Error fetching citations by agent memory: {str(e)}")
            raise
    
    async def get_citations_by_similarity_threshold(self, log_id: UUID, threshold: float) -> List[MessageCitationResponse]:
        """
        Get citations above a similarity threshold for a specific log
        
        Args:
            log_id: UUID of the conversation log
            threshold: Minimum similarity score
            
        Returns:
            List of message citation records
        """
        try:
            logger.debug(f"Fetching citations for log {log_id} with threshold {threshold}")
            response = await self.supabase.table(self.table_name).select("*").eq("log_id", str(log_id)).gte("similarity_score", threshold).execute()
            items = []
            for item in response.data:
                items.append(self.model_class(**item))
            return items
        except Exception as e:
            logger.error(f"Error fetching citations by similarity threshold: {str(e)}")
            raise


class ConversationCRUD:
    """Composite CRUD for conversations with citations"""
    
    def __init__(self, supabase: SupabaseClient):
        self.log_crud = ConversationLogCRUD(supabase)
        self.citation_crud = MessageCitationCRUD(supabase)
    
    async def get_messages_with_citations(self, agent_id: UUID, limit: int = 50) -> List[MessageWithCitations]:
        """
        Get conversation messages with their citations
        
        Args:
            agent_id: UUID of the agent
            limit: Maximum number of messages to return
            
        Returns:
            List of messages with citations
        """
        try:
            logger.debug(f"Fetching messages with citations for agent {agent_id}")
            logs = await self.log_crud.get_recent_logs(agent_id, limit)
            messages = []
            
            for log in logs:
                citations = await self.citation_crud.get_citations_by_log(log.id)
                messages.append(MessageWithCitations(log=log, citations=citations))
            
            return messages
        except Exception as e:
            logger.error(f"Error fetching messages with citations: {str(e)}")
            raise

