"""
Audio Utilities

Utility functions for audio processing.
"""

import numpy as np
from typing import Optional, Tuple

from app.telemetries.logger import logger


def bytes_to_numpy(audio_bytes: bytes, dtype=np.int16) -> np.ndarray:
    """
    Convert audio bytes to numpy array
    
    Args:
        audio_bytes: Raw audio bytes
        dtype: Data type for numpy array
        
    Returns:
        Numpy array
    """
    return np.frombuffer(audio_bytes, dtype=dtype)


def numpy_to_bytes(audio_array: np.ndarray) -> bytes:
    """
    Convert numpy array to audio bytes
    
    Args:
        audio_array: Numpy audio array
        
    Returns:
        Audio bytes
    """
    return audio_array.tobytes()


def normalize_audio(audio_data: np.ndarray) -> np.ndarray:
    """
    Normalize audio amplitude
    
    Args:
        audio_data: Audio numpy array
        
    Returns:
        Normalized audio array
    """
    if audio_data.dtype == np.int16:
        audio_data = audio_data.astype(np.float32) / 32768.0
    
    max_val = np.abs(audio_data).max()
    if max_val > 0:
        audio_data = audio_data / max_val
    
    return audio_data


def resample_audio(audio_data: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
    """
    Resample audio to target sample rate
    
    Args:
        audio_data: Audio numpy array
        orig_sr: Original sample rate
        target_sr: Target sample rate
        
    Returns:
        Resampled audio array
    """
    # TODO: Implement proper resampling (e.g., using librosa or scipy)
    logger.warning("Audio resampling not fully implemented")
    return audio_data


def calculate_rms(audio_data: np.ndarray) -> float:
    """
    Calculate RMS (Root Mean Square) of audio
    
    Args:
        audio_data: Audio numpy array
        
    Returns:
        RMS value
    """
    return np.sqrt(np.mean(audio_data ** 2))


def detect_silence(audio_data: np.ndarray, threshold: float = 0.01) -> bool:
    """
    Detect if audio is silent
    
    Args:
        audio_data: Audio numpy array
        threshold: Silence threshold
        
    Returns:
        True if silent
    """
    rms = calculate_rms(audio_data)
    return rms < threshold


def split_audio_chunks(audio_data: bytes, chunk_size: int = 1024) -> list[bytes]:
    """
    Split audio data into chunks
    
    Args:
        audio_data: Raw audio bytes
        chunk_size: Size of each chunk
        
    Returns:
        List of audio chunks
    """
    chunks = []
    for i in range(0, len(audio_data), chunk_size):
        chunks.append(audio_data[i:i + chunk_size])
    return chunks


def merge_audio_chunks(chunks: list[bytes]) -> bytes:
    """
    Merge audio chunks into single audio data
    
    Args:
        chunks: List of audio chunks
        
    Returns:
        Merged audio bytes
    """
    return b''.join(chunks)
