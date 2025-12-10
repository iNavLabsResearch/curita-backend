"""
Agent tools service for managing agent tools
"""
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

from app.data_layer.supabase_client import get_supabase
from app.services.base import BaseService


class AgentToolsService(BaseService):
    """Service for managing agent tools with JSON schema support"""
    
    def __init__(self):
        """Initialize agent tools service"""
        super().__init__()
        self.table_name = self.settings.AGENT_TOOLS_TABLE
        self.supabase = None
        self.initialize()
    
    def initialize(self):
        """Initialize service resources"""
        self.logger.info(f"Initializing agent tools service for table: {self.table_name}")
        self.supabase = get_supabase()
        self.logger.info("Agent tools service initialized successfully")
    
    def create(self, tool_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new agent tool
        
        Args:
            tool_data: Tool data with JSON schemas
            
        Returns:
            Created tool record
        """
        self.logger.info(f"Creating agent tool: {tool_data.get('name')} for toy: {tool_data.get('toy_id')}")
        
        # Validate required schemas
        if "tool_schema" not in tool_data:
            raise ValueError("tool_schema is required")
        
        # Add timestamps
        tool_data["created_at"] = datetime.utcnow().isoformat()
        tool_data["updated_at"] = datetime.utcnow().isoformat()
        
        response = self.supabase.table(self.table_name).insert(tool_data).execute()
        
        self.logger.info(f"Agent tool created successfully: {response.data[0]['id']}")
        return response.data[0]
    
    def get_by_id(self, tool_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get tool by ID
        
        Args:
            tool_id: Tool UUID
            
        Returns:
            Tool record or None
        """
        self.logger.info(f"Fetching tool: {tool_id}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("id", str(tool_id))\
            .execute()
        
        if response.data:
            return response.data[0]
        
        self.logger.warning(f"Tool not found: {tool_id}")
        return None
    
    def list_by_toy(self, toy_id: UUID) -> List[Dict[str, Any]]:
        """
        List tools for a specific toy
        
        Args:
            toy_id: Toy UUID
            
        Returns:
            List of tool records
        """
        self.logger.info(f"Listing tools for toy: {toy_id}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("toy_id", str(toy_id))\
            .order("created_at", desc=True)\
            .execute()
        
        self.logger.debug(f"Retrieved {len(response.data)} tools for toy {toy_id}")
        return response.data
    
    def list_by_provider(self, provider_name: str) -> List[Dict[str, Any]]:
        """
        List tools by provider name
        
        Args:
            provider_name: Provider name
            
        Returns:
            List of tool records
        """
        self.logger.info(f"Listing tools for provider: {provider_name}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("provider_name", provider_name)\
            .order("created_at", desc=True)\
            .execute()
        
        self.logger.debug(f"Retrieved {len(response.data)} tools for provider {provider_name}")
        return response.data
    
    def list(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        List all tools with pagination
        
        Args:
            limit: Maximum number of records
            offset: Number of records to skip
            
        Returns:
            List of tool records
        """
        self.logger.info(f"Listing tools: limit={limit}, offset={offset}")
        
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .order("created_at", desc=True)\
            .range(offset, offset + limit - 1)\
            .execute()
        
        self.logger.debug(f"Retrieved {len(response.data)} tools")
        return response.data
    
    def update(self, tool_id: UUID, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update tool
        
        Args:
            tool_id: Tool UUID
            updates: Fields to update
            
        Returns:
            Updated tool record or None
        """
        self.logger.info(f"Updating tool: {tool_id}")
        
        # Add updated timestamp
        updates["updated_at"] = datetime.utcnow().isoformat()
        
        response = self.supabase.table(self.table_name)\
            .update(updates)\
            .eq("id", str(tool_id))\
            .execute()
        
        if response.data:
            self.logger.info(f"Tool updated successfully: {tool_id}")
            return response.data[0]
        
        self.logger.warning(f"Tool not found for update: {tool_id}")
        return None
    
    def update_schema(
        self,
        tool_id: UUID,
        tool_schema: Optional[Dict[str, Any]] = None,
        payload_schema: Optional[Dict[str, Any]] = None,
        headers_schema: Optional[Dict[str, Any]] = None,
        output_schema: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Update tool schemas
        
        Args:
            tool_id: Tool UUID
            tool_schema: Tool schema
            payload_schema: Payload schema
            headers_schema: Headers schema
            output_schema: Output schema
            
        Returns:
            Updated tool record or None
        """
        self.logger.info(f"Updating schemas for tool: {tool_id}")
        
        updates = {}
        if tool_schema is not None:
            updates["tool_schema"] = tool_schema
        if payload_schema is not None:
            updates["payload_schema"] = payload_schema
        if headers_schema is not None:
            updates["headers_schema"] = headers_schema
        if output_schema is not None:
            updates["output_schema"] = output_schema
        
        if not updates:
            self.logger.warning("No schema updates provided")
            return None
        
        return self.update(tool_id, updates)
    
    def delete(self, tool_id: UUID) -> bool:
        """
        Delete tool
        
        Args:
            tool_id: Tool UUID
            
        Returns:
            True if deleted, False otherwise
        """
        self.logger.info(f"Deleting tool: {tool_id}")
        
        response = self.supabase.table(self.table_name)\
            .delete()\
            .eq("id", str(tool_id))\
            .execute()
        
        success = len(response.data) > 0
        if success:
            self.logger.info(f"Tool deleted successfully: {tool_id}")
        else:
            self.logger.warning(f"Tool not found for deletion: {tool_id}")
        
        return success


def get_agent_tools_service() -> AgentToolsService:
    """Get agent tools service instance"""
    return AgentToolsService()
