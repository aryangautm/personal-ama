from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PersonaBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    public_name: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str] = None
    tagline: Optional[str] = Field(None, max_length=100)
    prompt: Optional[str] = None
    welcome_message: Optional[str] = None
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(500, gt=0)
    llm_provider: str = Field("google", max_length=20)
    llm_model: Optional[str] = Field(None, max_length=50)
    profile_image_url: Optional[str] = Field(None, max_length=512)
    social_links: Optional[Dict[str, Any]] = None
    custom_settings: Optional[Dict[str, Any]] = None
    is_active: bool = True


class PersonaCreate(PersonaBase):
    pass


class PersonaUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=50)
    public_name: Optional[str] = Field(None, min_length=1, max_length=100)
    bio: Optional[str] = None
    tagline: Optional[str] = Field(None, max_length=100)
    prompt: Optional[str] = None
    welcome_message: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, gt=0)
    llm_provider: Optional[str] = Field(None, max_length=20)
    llm_model: Optional[str] = Field(None, max_length=50)
    profile_image_url: Optional[str] = Field(None, max_length=512)
    social_links: Optional[Dict[str, Any]] = None
    custom_settings: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class PersonaResponse(PersonaBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
