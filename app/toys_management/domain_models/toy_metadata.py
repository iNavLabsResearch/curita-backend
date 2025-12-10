"""
Toy Metadata

Metadata structures for toy entities.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class ToyMetadata:
    """
    Metadata for a toy entity
    """
    
    toy_id: UUID
    name: str
    toy_type: str
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    firmware_version: Optional[str] = None
    hardware_version: Optional[str] = None
    serial_number: Optional[str] = None
    
    # Capabilities
    capabilities: List[str] = field(default_factory=list)
    supported_languages: List[str] = field(default_factory=lambda: ["en-US"])
    
    # Status
    is_active: bool = True
    is_online: bool = False
    last_seen: Optional[datetime] = None
    connection_status: str = "disconnected"
    
    # Configuration references
    agent_id: Optional[UUID] = None
    memory_enabled: bool = True
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    # Additional metadata
    tags: List[str] = field(default_factory=list)
    custom_properties: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "toy_id": str(self.toy_id),
            "name": self.name,
            "toy_type": self.toy_type,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "firmware_version": self.firmware_version,
            "hardware_version": self.hardware_version,
            "serial_number": self.serial_number,
            "capabilities": self.capabilities,
            "supported_languages": self.supported_languages,
            "is_active": self.is_active,
            "is_online": self.is_online,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "connection_status": self.connection_status,
            "agent_id": str(self.agent_id) if self.agent_id else None,
            "memory_enabled": self.memory_enabled,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "tags": self.tags,
            "custom_properties": self.custom_properties
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ToyMetadata":
        """Create from dictionary"""
        return cls(
            toy_id=UUID(data["toy_id"]) if isinstance(data["toy_id"], str) else data["toy_id"],
            name=data["name"],
            toy_type=data["toy_type"],
            manufacturer=data.get("manufacturer"),
            model=data.get("model"),
            firmware_version=data.get("firmware_version"),
            hardware_version=data.get("hardware_version"),
            serial_number=data.get("serial_number"),
            capabilities=data.get("capabilities", []),
            supported_languages=data.get("supported_languages", ["en-US"]),
            is_active=data.get("is_active", True),
            is_online=data.get("is_online", False),
            last_seen=datetime.fromisoformat(data["last_seen"]) if data.get("last_seen") else None,
            connection_status=data.get("connection_status", "disconnected"),
            agent_id=UUID(data["agent_id"]) if data.get("agent_id") else None,
            memory_enabled=data.get("memory_enabled", True),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.utcnow(),
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else datetime.utcnow(),
            tags=data.get("tags", []),
            custom_properties=data.get("custom_properties", {})
        )
