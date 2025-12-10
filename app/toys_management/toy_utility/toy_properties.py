"""
Toy Properties

Defines and handles toy property definitions and configurations.
"""

from typing import Dict, Any, List, Optional
from enum import Enum

from app.telemetries.logger import logger


class ToyCapability(Enum):
    """Toy capability types"""
    VOICE_INPUT = "voice_input"
    VOICE_OUTPUT = "voice_output"
    TEXT_DISPLAY = "text_display"
    MOTION_CONTROL = "motion_control"
    LIGHT_EFFECTS = "light_effects"
    TOUCH_SENSORS = "touch_sensors"
    CAMERA = "camera"


class ToyProperties:
    """
    Manages toy properties and capabilities
    """
    
    def __init__(self, toy_config: Dict[str, Any]):
        """
        Initialize toy properties
        
        Args:
            toy_config: Toy configuration dictionary
        """
        self.config = toy_config
        self.toy_id = toy_config.get("id")
        self.name = toy_config.get("name", "Unknown")
        self.capabilities = self._parse_capabilities(toy_config.get("capabilities", []))
        self.properties = toy_config.get("properties", {})
        
        logger.debug(f"Initialized properties for toy: {self.name}")
    
    def _parse_capabilities(self, capabilities: List[str]) -> List[ToyCapability]:
        """
        Parse capability strings to enum
        
        Args:
            capabilities: List of capability strings
            
        Returns:
            List of ToyCapability enums
        """
        parsed = []
        for cap in capabilities:
            try:
                parsed.append(ToyCapability(cap))
            except ValueError:
                logger.warning(f"Unknown capability: {cap}")
        return parsed
    
    def has_capability(self, capability: ToyCapability) -> bool:
        """
        Check if toy has specific capability
        
        Args:
            capability: Capability to check
            
        Returns:
            True if toy has capability
        """
        return capability in self.capabilities
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """
        Get property value
        
        Args:
            key: Property key
            default: Default value if not found
            
        Returns:
            Property value
        """
        return self.properties.get(key, default)
    
    def set_property(self, key: str, value: Any) -> None:
        """
        Set property value
        
        Args:
            key: Property key
            value: Property value
        """
        self.properties[key] = value
        logger.debug(f"Set property {key} for toy {self.name}")
    
    def get_audio_config(self) -> Dict[str, Any]:
        """
        Get audio configuration
        
        Returns:
            Audio configuration dictionary
        """
        return {
            "sample_rate": self.get_property("audio_sample_rate", 16000),
            "channels": self.get_property("audio_channels", 1),
            "format": self.get_property("audio_format", "pcm"),
            "codec": self.get_property("audio_codec", "opus")
        }
    
    def get_voice_config(self) -> Dict[str, Any]:
        """
        Get voice configuration for TTS
        
        Returns:
            Voice configuration dictionary
        """
        return {
            "voice_id": self.get_property("voice_id"),
            "voice_name": self.get_property("voice_name", "default"),
            "language": self.get_property("language", "en-US"),
            "speaking_rate": self.get_property("speaking_rate", 1.0),
            "pitch": self.get_property("pitch", 0.0)
        }
    
    def validate(self) -> tuple[bool, List[str]]:
        """
        Validate toy properties
        
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        if not self.toy_id:
            errors.append("Toy ID is required")
        
        if not self.name or self.name == "Unknown":
            errors.append("Toy name is required")
        
        if not self.capabilities:
            errors.append("At least one capability is required")
        
        return len(errors) == 0, errors
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary
        
        Returns:
            Properties as dictionary
        """
        return {
            "toy_id": str(self.toy_id),
            "name": self.name,
            "capabilities": [cap.value for cap in self.capabilities],
            "properties": self.properties,
            "audio_config": self.get_audio_config(),
            "voice_config": self.get_voice_config()
        }
