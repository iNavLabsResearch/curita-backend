"""
Conversation service for managing conversation logs
"""
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

from app.data_layer.supabase_client import get_supabase
from app.services.base import BaseService


class ConversationService(BaseService):
    """Service for managing conversation logs"""
    
    VALID_ROLES = {"user", "assistant", "system", "tool"}
    
    def __init__(self):
        """Initialize conversation service"""
        super().__init__()
        self.table_name = self.settings.CONVERSATION_LOGS_TABLE
        self.supabase = None
        self.initialize()
    
    def initialize(self):
        """Initialize service resources"""
        self.logger.info(f"Initializing conversation service for table: {self.table_name}")
        self.supabase = get_supabase()
        self.logger.info("Conversation service initialized successfully")
    
    def add_message(
        self,
        agent_id: UUID,
        role: str,
        content: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add a message to conversation log
        
        Args:
            agent_id: Agent UUID
            role: Message role (user, assistant, system, tool)
            content: Message content
            
        Returns:
            Created log record
        """
        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role: {role}. Must be one of {self.VALID_ROLES}")
        
        self.logger.info(f"Adding message to conversation: agent={agent_id}, role={role}")
        
        message_data = {
            "agent_id": str(agent_id),
            "role": role,
            "content": content,
            "created_at": datetime.utcnow().isoformat()
        }
        
        response = self.supabase.table(self.table_name).insert(message_data).execute()
        
        self.logger.info(f"Message added to conversation: {response.data[0]['id']}")
        return response.data[0]
    
    def get_by_agent(
        self,
        agent_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history for an agent
        
        Args:
            agent_id: Agent UUID
            limit: Maximum number of messages
            offset: Number of messages to skip
            
        Returns:
            List of conversation messages
        """
        self.logger.info(f"Fetching conversation history: agent={agent_id}, limit={limit}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("agent_id", str(agent_id))\
            .order("created_at", desc=False)\
            .range(offset, offset + limit - 1)\
            .execute()
        
        self.logger.debug(f"Retrieved {len(response.data)} messages for agent {agent_id}")
        return response.data
    
    def get_recent(
        self,
        agent_id: UUID,
        count: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recent conversation messages
        
        Args:
            agent_id: Agent UUID
            count: Number of recent messages
            
        Returns:
            List of recent messages
        """
        self.logger.info(f"Fetching recent messages: agent={agent_id}, count={count}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("agent_id", str(agent_id))\
            .order("created_at", desc=True)\
            .limit(count)\
            .execute()
        
        # Reverse to get chronological order
        messages = list(reversed(response.data))
        
        self.logger.debug(f"Retrieved {len(messages)} recent messages")
        return messages
    
    def get_by_id(self, log_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get a specific conversation log
        
        Args:
            log_id: Log UUID
            
        Returns:
            Log record or None
        """
        self.logger.info(f"Fetching conversation log: {log_id}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("id", str(log_id))\
            .execute()
        
        if response.data:
            return response.data[0]
        
        self.logger.warning(f"Conversation log not found: {log_id}")
        return None
    
    def get_by_role(
        self,
        agent_id: UUID,
        role: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get messages by role
        
        Args:
            agent_id: Agent UUID
            role: Message role
            limit: Maximum number of messages
            
        Returns:
            List of messages with specified role
        """
        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role: {role}. Must be one of {self.VALID_ROLES}")
        
        self.logger.info(f"Fetching messages by role: agent={agent_id}, role={role}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("agent_id", str(agent_id))\
            .eq("role", role)\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        
        self.logger.debug(f"Retrieved {len(response.data)} messages with role {role}")
        return response.data
    
    def delete_by_agent(self, agent_id: UUID) -> bool:
        """
        Delete all conversation logs for an agent
        
        Args:
            agent_id: Agent UUID
            
        Returns:
            True if deleted
        """
        self.logger.info(f"Deleting conversation logs for agent: {agent_id}")
        
        response = self.supabase.table(self.table_name)\
            .delete()\
            .eq("agent_id", str(agent_id))\
            .execute()
        
        self.logger.info(f"Conversation logs deleted for agent: {agent_id}")
        return True
    
    def delete_by_id(self, log_id: UUID) -> bool:
        """
        Delete a specific conversation log
        
        Args:
            log_id: Log UUID
            
        Returns:
            True if deleted, False otherwise
        """
        self.logger.info(f"Deleting conversation log: {log_id}")
        
        response = self.supabase.table(self.table_name)\
            .delete()\
            .eq("id", str(log_id))\
            .execute()
        
        success = len(response.data) > 0
        if success:
            self.logger.info(f"Conversation log deleted: {log_id}")
        else:
            self.logger.warning(f"Conversation log not found: {log_id}")
        
        return success
    
    def clear_history(
        self,
        agent_id: UUID,
        keep_system: bool = True
    ) -> bool:
        """
        Clear conversation history
        
        Args:
            agent_id: Agent UUID
            keep_system: Keep system messages
            
        Returns:
            True if cleared
        """
        self.logger.info(f"Clearing conversation history: agent={agent_id}, keep_system={keep_system}")
        
        query = self.supabase.table(self.table_name)\
            .delete()\
            .eq("agent_id", str(agent_id))
        
        if keep_system:
            query = query.neq("role", "system")
        
        response = query.execute()
        
        self.logger.info(f"Conversation history cleared for agent: {agent_id}")
        return True


def get_conversation_service() -> ConversationService:
    """Get conversation service instance"""
    return ConversationService()
