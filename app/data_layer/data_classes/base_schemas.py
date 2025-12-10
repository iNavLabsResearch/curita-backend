"""
Base schemas used across all data classes
"""
from pydantic import BaseModel, Field
from typing import Optional, Any, List


class BaseResponse(BaseModel):
    """Base response model"""
    success: bool
    message: Optional[str] = None


class PaginationParams(BaseModel):
    """Pagination parameters"""
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)


class ListResponse(BaseResponse):
    """Generic list response"""
    items: List[Any]
    count: int
    limit: int
    offset: int
