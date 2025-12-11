"""
Toy schemas for toy entities
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class ToyBase(BaseModel):
    """Base schema for toy"""
    name: str = Field(..., description="Name of the toy")
    description: Optional[str] = Field(None, description="Description of the toy")
    avatar_url: Optional[str] = Field(None, description="URL to toy avatar image")
    user_custom_instruction: Optional[str] = Field(None, description="Custom user instructions for the toy")
    is_active: bool = Field(True, description="Whether the toy is active")


class ToyCreate(ToyBase):
    """Schema for creating toy"""
    pass


class ToyUpdate(BaseModel):
    """Schema for updating toy"""
    name: Optional[str] = None
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    user_custom_instruction: Optional[str] = None
    is_active: Optional[bool] = None


class ToyResponse(ToyBase):
    """Schema for toy response"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
