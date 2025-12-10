"""
Toy Configuration

Configuration models for toy setup and behavior.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class AudioConfiguration:
    """Audio configuration for toy"""
    sample_rate: int = 16000
    channels: int = 1
    format: str = "pcm"
    codec: str = "opus"
    bit_depth: int = 16
    
    # Noise reduction
    noise_reduction_enabled: bool = True
    echo_cancellation_enabled: bool = True
    
    # Volume settings
    input_volume: float = 1.0
    output_volume: float = 1.0


@dataclass
class VoiceConfiguration:
    """Voice configuration for TTS"""
    provider: str = "openai"
    voice_id: Optional[str] = None
    voice_name: str = "default"
    language: str = "en-US"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    emotion: Optional[str] = None


@dataclass
class ConversationConfiguration:
    """Conversation behavior configuration"""
    max_history_length: int = 50
    context_window: int = 10
    enable_memory: bool = True
    enable_citations: bool = True
    
    # Response behavior
    max_response_length: int = 500
    temperature: float = 0.7
    response_timeout_seconds: int = 30


@dataclass
class ToyConfiguration:
    """
    Complete configuration for a toy
    """
    
    toy_id: UUID
    name: str
    
    # Agent configuration
    agent_id: Optional[UUID] = None
    personality: str = "friendly"
    
    # Audio/Voice
    audio: AudioConfiguration = field(default_factory=AudioConfiguration)
    voice: VoiceConfiguration = field(default_factory=VoiceConfiguration)
    
    # Conversation
    conversation: ConversationConfiguration = field(default_factory=ConversationConfiguration)
    
    # Feature flags
    features: Dict[str, bool] = field(default_factory=lambda: {
        "voice_input": True,
        "voice_output": True,
        "text_display": False,
        "emotion_detection": True,
        "multi_language": False
    })
    
    # Advanced settings
    advanced: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "toy_id": str(self.toy_id),
            "name": self.name,
            "agent_id": str(self.agent_id) if self.agent_id else None,
            "personality": self.personality,
            "audio": {
                "sample_rate": self.audio.sample_rate,
                "channels": self.audio.channels,
                "format": self.audio.format,
                "codec": self.audio.codec,
                "bit_depth": self.audio.bit_depth,
                "noise_reduction_enabled": self.audio.noise_reduction_enabled,
                "echo_cancellation_enabled": self.audio.echo_cancellation_enabled,
                "input_volume": self.audio.input_volume,
                "output_volume": self.audio.output_volume
            },
            "voice": {
                "provider": self.voice.provider,
                "voice_id": self.voice.voice_id,
                "voice_name": self.voice.voice_name,
                "language": self.voice.language,
                "speaking_rate": self.voice.speaking_rate,
                "pitch": self.voice.pitch,
                "emotion": self.voice.emotion
            },
            "conversation": {
                "max_history_length": self.conversation.max_history_length,
                "context_window": self.conversation.context_window,
                "enable_memory": self.conversation.enable_memory,
                "enable_citations": self.conversation.enable_citations,
                "max_response_length": self.conversation.max_response_length,
                "temperature": self.conversation.temperature,
                "response_timeout_seconds": self.conversation.response_timeout_seconds
            },
            "features": self.features,
            "advanced": self.advanced
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ToyConfiguration":
        """Create from dictionary"""
        audio_data = data.get("audio", {})
        voice_data = data.get("voice", {})
        conversation_data = data.get("conversation", {})
        
        return cls(
            toy_id=UUID(data["toy_id"]) if isinstance(data["toy_id"], str) else data["toy_id"],
            name=data["name"],
            agent_id=UUID(data["agent_id"]) if data.get("agent_id") else None,
            personality=data.get("personality", "friendly"),
            audio=AudioConfiguration(
                sample_rate=audio_data.get("sample_rate", 16000),
                channels=audio_data.get("channels", 1),
                format=audio_data.get("format", "pcm"),
                codec=audio_data.get("codec", "opus"),
                bit_depth=audio_data.get("bit_depth", 16),
                noise_reduction_enabled=audio_data.get("noise_reduction_enabled", True),
                echo_cancellation_enabled=audio_data.get("echo_cancellation_enabled", True),
                input_volume=audio_data.get("input_volume", 1.0),
                output_volume=audio_data.get("output_volume", 1.0)
            ),
            voice=VoiceConfiguration(
                provider=voice_data.get("provider", "openai"),
                voice_id=voice_data.get("voice_id"),
                voice_name=voice_data.get("voice_name", "default"),
                language=voice_data.get("language", "en-US"),
                speaking_rate=voice_data.get("speaking_rate", 1.0),
                pitch=voice_data.get("pitch", 0.0),
                emotion=voice_data.get("emotion")
            ),
            conversation=ConversationConfiguration(
                max_history_length=conversation_data.get("max_history_length", 50),
                context_window=conversation_data.get("context_window", 10),
                enable_memory=conversation_data.get("enable_memory", True),
                enable_citations=conversation_data.get("enable_citations", True),
                max_response_length=conversation_data.get("max_response_length", 500),
                temperature=conversation_data.get("temperature", 0.7),
                response_timeout_seconds=conversation_data.get("response_timeout_seconds", 30)
            ),
            features=data.get("features", {
                "voice_input": True,
                "voice_output": True,
                "text_display": False,
                "emotion_detection": True,
                "multi_language": False
            }),
            advanced=data.get("advanced", {})
        )
