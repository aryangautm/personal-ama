import uuid
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func

from app.models.base import Base


class Persona(Base):
    """
    AI Persona model.

    Each persona has a unique username
    Stores configuration for AI behavior, appearance, and settings.
    """

    __tablename__ = "personas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    public_name = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)
    tagline = Column(String(100), nullable=True)

    # AI Configuration
    prompt = Column(Text, nullable=True)
    welcome_message = Column(Text, nullable=True)
    temperature = Column(Float, default=0.7, nullable=False)
    max_tokens = Column(Integer, default=500, nullable=False)
    llm_provider = Column(String(20), default="google", nullable=False)
    llm_model = Column(String(50), nullable=True)

    # Display Settings
    profile_image_url = Column(String(512), nullable=True)
    social_links = Column(JSONB, nullable=True)
    # Format: {"twitter": "url", "linkedin": "url", ...}
    custom_settings = Column(JSONB, nullable=True)
    # Any additional customization

    # Status
    is_active = Column(Boolean, default=True, nullable=False, index=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self):
        return f"<Persona(id={self.id}, username={self.username})>"
