"""
Conversation Model

SQLModel representation of a chat conversation session.
"""

from datetime import datetime
from typing import Optional
import uuid

from sqlmodel import Field, SQLModel


def generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid.uuid4())


class Conversation(SQLModel, table=True):
    """Conversation database model."""

    __tablename__ = "conversations"

    id: str = Field(
        default_factory=generate_uuid,
        primary_key=True,
        max_length=36,
        description="Unique conversation identifier"
    )
    user_id: str = Field(max_length=100, index=True, description="Owner's external user ID")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Session start timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last activity timestamp")


class ConversationResponse(SQLModel):
    """Schema for conversation API responses."""

    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
