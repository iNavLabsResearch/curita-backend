"""
Domain models for provider types
"""
from enum import Enum


class ProviderType(str, Enum):
    """Types of providers in the system"""
    MODEL = "model"  # LLM providers
    TTS = "tts"  # Text-to-speech providers
    TRANSCRIBER = "transcriber"  # Speech-to-text providers


class ProviderName(str, Enum):
    """Common provider names"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    AZURE = "azure"
    ELEVENLABS = "elevenlabs"
    CARTESIA = "cartesia"
    DEEPGRAM = "deepgram"
    WHISPER = "whisper"
