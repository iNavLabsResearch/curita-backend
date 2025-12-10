"""
Speech Processor Module

Handles speech processing, VAD, and audio preprocessing.
"""

from app.services.speech_processor.vad.vad_processor import VADProcessor

__all__ = [
    "VADProcessor",
]
