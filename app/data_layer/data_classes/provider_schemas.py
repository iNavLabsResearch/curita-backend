"""
Provider schemas for model, TTS, and transcriber providers
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# ============================================================================
# MODEL PROVIDER SCHEMAS
# ============================================================================

class ModelProviderBase(BaseModel):
    """Base schema for model provider"""
    provider_name: str
    model_name: str
    is_large_model: bool = False
    default_temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    supported_languages: List[str] = ["en"]
    api_key_template: Optional[str] = None
    api_base: Optional[str] = None
    api_key: Optional[str] = None
    is_default: bool = False


class ModelProviderCreate(ModelProviderBase):
    """Schema for creating model provider"""
    pass


class ModelProviderUpdate(BaseModel):
    """Schema for updating model provider"""
    provider_name: Optional[str] = None
    model_name: Optional[str] = None
    is_large_model: Optional[bool] = None
    default_temperature: Optional[float] = None
    supported_languages: Optional[List[str]] = None
    api_key_template: Optional[str] = None
    api_base: Optional[str] = None
    api_key: Optional[str] = None
    is_default: Optional[bool] = None


class ModelProviderResponse(ModelProviderBase):
    """Schema for model provider response"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# TTS PROVIDER SCHEMAS
# ============================================================================

class TTSProviderBase(BaseModel):
    """Base schema for TTS provider"""
    provider_name: str
    model_name: str
    supported_languages: List[str] = ["en"]
    requires_api_key: bool = True
    default_endpoint: Optional[str] = None
    api_key_template: Optional[str] = None
    api_key: Optional[str] = None
    is_default: bool = False
    default_voice: Optional[str] = None


class TTSProviderCreate(TTSProviderBase):
    """Schema for creating TTS provider"""
    pass


class TTSProviderUpdate(BaseModel):
    """Schema for updating TTS provider"""
    provider_name: Optional[str] = None
    model_name: Optional[str] = None
    supported_languages: Optional[List[str]] = None
    requires_api_key: Optional[bool] = None
    default_endpoint: Optional[str] = None
    api_key_template: Optional[str] = None
    api_key: Optional[str] = None
    is_default: Optional[bool] = None
    default_voice: Optional[str] = None


class TTSProviderResponse(TTSProviderBase):
    """Schema for TTS provider response"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# TRANSCRIBER PROVIDER SCHEMAS
# ============================================================================

class TranscriberProviderBase(BaseModel):
    """Base schema for transcriber provider"""
    name: Optional[str] = None
    provider_name: str
    model_name: str
    supported_languages: List[str] = ["en"]
    requires_api_key: bool = True
    default_endpoint: Optional[str] = None
    api_key_template: Optional[str] = None
    model_size: Optional[str] = None
    is_default: bool = False
    api_key: Optional[str] = None


class TranscriberProviderCreate(TranscriberProviderBase):
    """Schema for creating transcriber provider"""
    pass


class TranscriberProviderUpdate(BaseModel):
    """Schema for updating transcriber provider"""
    name: Optional[str] = None
    provider_name: Optional[str] = None
    model_name: Optional[str] = None
    supported_languages: Optional[List[str]] = None
    requires_api_key: Optional[bool] = None
    default_endpoint: Optional[str] = None
    api_key_template: Optional[str] = None
    model_size: Optional[str] = None
    is_default: Optional[bool] = None
    api_key: Optional[str] = None


class TranscriberProviderResponse(TranscriberProviderBase):
    """Schema for transcriber provider response"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
