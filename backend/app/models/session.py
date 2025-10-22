import uuid
from datetime import datetime

from .base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    persona_id = Column(UUID(as_uuid=True), ForeignKey("personas.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    messages = relationship("ChatMessage", back_populates="session", lazy="dynamic")

    def __repr__(self):
        return f"<Session(id='{self.id}', persona_id='{self.persona_id}')>"


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)

    role = Column(String(50))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.now, index=True)

    session = relationship("Session", back_populates="messages")
