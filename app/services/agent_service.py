"""
Agent service for managing agents
"""
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

from app.utilities.supabase_client import get_supabase
from app.services.base import BaseService


class AgentService(BaseService):
    """Service for managing agents"""
    
    def __init__(self):
        """Initialize agent service"""
        super().__init__()
        self.table_name = self.settings.AGENTS_TABLE
        self.supabase = None
        self.initialize()
    
    def initialize(self):
        """Initialize service resources"""
        self.logger.info(f"Initializing agent service for table: {self.table_name}")
        self.supabase = get_supabase()
        self.logger.info("Agent service initialized successfully")
    
    def create(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new agent
        
        Args:
            agent_data: Agent data with provider links
            
        Returns:
            Created agent record
        """
        self.logger.info(f"Creating agent: {agent_data.get('name')} for toy: {agent_data.get('toy_id')}")
        
        # Add timestamps
        agent_data["created_at"] = datetime.utcnow().isoformat()
        agent_data["updated_at"] = datetime.utcnow().isoformat()
        
        response = self.supabase.table(self.table_name).insert(agent_data).execute()
        
        self.logger.info(f"Agent created successfully: {response.data[0]['id']}")
        return response.data[0]
    
    def get_by_id(self, agent_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get agent by ID
        
        Args:
            agent_id: Agent UUID
            
        Returns:
            Agent record or None
        """
        self.logger.info(f"Fetching agent: {agent_id}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("id", str(agent_id))\
            .execute()
        
        if response.data:
            return response.data[0]
        
        self.logger.warning(f"Agent not found: {agent_id}")
        return None
    
    def get_with_providers(self, agent_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get agent with provider details
        
        Args:
            agent_id: Agent UUID
            
        Returns:
            Agent record with provider details or None
        """
        self.logger.info(f"Fetching agent with providers: {agent_id}")
        
        response = self.supabase.table(self.table_name)\
            .select("*, model_providers(*), tts_providers(*), transcriber_providers(*)")\
            .eq("id", str(agent_id))\
            .execute()
        
        if response.data:
            return response.data[0]
        
        self.logger.warning(f"Agent not found: {agent_id}")
        return None
    
    def list_by_toy(self, toy_id: UUID, is_active: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        List agents for a specific toy
        
        Args:
            toy_id: Toy UUID
            is_active: Filter by active status
            
        Returns:
            List of agent records
        """
        self.logger.info(f"Listing agents for toy: {toy_id}, is_active={is_active}")
        
        query = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("toy_id", str(toy_id))
        
        if is_active is not None:
            query = query.eq("is_active", is_active)
        
        response = query.order("created_at", desc=True).execute()
        
        self.logger.debug(f"Retrieved {len(response.data)} agents for toy {toy_id}")
        return response.data
    
    def list(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        List all agents with pagination
        
        Args:
            limit: Maximum number of records
            offset: Number of records to skip
            
        Returns:
            List of agent records
        """
        self.logger.info(f"Listing agents: limit={limit}, offset={offset}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .order("created_at", desc=True)\
            .range(offset, offset + limit - 1)\
            .execute()
        
        self.logger.debug(f"Retrieved {len(response.data)} agents")
        return response.data
    
    def update(self, agent_id: UUID, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update agent
        
        Args:
            agent_id: Agent UUID
            updates: Fields to update
            
        Returns:
            Updated agent record or None
        """
        self.logger.info(f"Updating agent: {agent_id}")
        
        # Add updated timestamp
        updates["updated_at"] = datetime.utcnow().isoformat()
        
        response = self.supabase.table(self.table_name)\
            .update(updates)\
            .eq("id", str(agent_id))\
            .execute()
        
        if response.data:
            self.logger.info(f"Agent updated successfully: {agent_id}")
            return response.data[0]
        
        self.logger.warning(f"Agent not found for update: {agent_id}")
        return None
    
    def delete(self, agent_id: UUID) -> bool:
        """
        Delete agent (will cascade to memories and conversation logs)
        
        Args:
            agent_id: Agent UUID
            
        Returns:
            True if deleted, False otherwise
        """
        self.logger.info(f"Deleting agent: {agent_id}")
        
        response = self.supabase.table(self.table_name)\
            .delete()\
            .eq("id", str(agent_id))\
            .execute()
        
        success = len(response.data) > 0
        if success:
            self.logger.info(f"Agent deleted successfully: {agent_id}")
        else:
            self.logger.warning(f"Agent not found for deletion: {agent_id}")
        
        return success
    
    def activate(self, agent_id: UUID, is_active: bool = True) -> Optional[Dict[str, Any]]:
        """
        Activate or deactivate an agent
        
        Args:
            agent_id: Agent UUID
            is_active: Activation status
            
        Returns:
            Updated agent record or None
        """
        self.logger.info(f"{'Activating' if is_active else 'Deactivating'} agent: {agent_id}")
        
        return self.update(agent_id, {"is_active": is_active})
    
    def update_providers(
        self,
        agent_id: UUID,
        model_provider_id: Optional[UUID] = None,
        tts_provider_id: Optional[UUID] = None,
        transcriber_provider_id: Optional[UUID] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Update agent provider links
        
        Args:
            agent_id: Agent UUID
            model_provider_id: Model provider UUID
            tts_provider_id: TTS provider UUID
            transcriber_provider_id: Transcriber provider UUID
            
        Returns:
            Updated agent record or None
        """
        self.logger.info(f"Updating providers for agent: {agent_id}")
        
        updates = {}
        if model_provider_id is not None:
            updates["model_provider_id"] = str(model_provider_id)
        if tts_provider_id is not None:
            updates["tts_provider_id"] = str(tts_provider_id)
        if transcriber_provider_id is not None:
            updates["transcriber_provider_id"] = str(transcriber_provider_id)
        
        if not updates:
            self.logger.warning("No provider updates provided")
            return None
        
        return self.update(agent_id, updates)


def get_agent_service() -> AgentService:
    """Get agent service instance"""
    return AgentService()
