"""
Message Model

SQLModel representation of a chat message.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional
import uuid

from sqlmodel import Field, SQLModel, Column
from sqlalchemy import JSON


def generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid.uuid4())


class MessageRole(str, Enum):
    """Message role enum."""

    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    """Message database model."""

    __tablename__ = "messages"

    id: str = Field(
        default_factory=generate_uuid,
        primary_key=True,
        max_length=36,
        description="Unique message identifier"
    )
    user_id: str = Field(max_length=100, description="Owner's external user ID")
    conversation_id: str = Field(
        max_length=36,
        foreign_key="conversations.id",
        description="Parent conversation"
    )
    role: MessageRole = Field(description="Message sender role")
    content: str = Field(max_length=10000, description="Message text content")
    tool_calls: Optional[list[dict[str, Any]]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="MCP tool calls made (assistant only)"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Message timestamp")


class MessageCreate(SQLModel):
    """Schema for creating a message."""

    role: MessageRole
    content: str = Field(max_length=10000)
    tool_calls: Optional[list[dict[str, Any]]] = None


class MessageResponse(SQLModel):
    """Schema for message API responses."""

    id: str
    user_id: str
    conversation_id: str
    role: MessageRole
    content: str
    tool_calls: Optional[list[dict[str, Any]]]
    created_at: datetime

    class Config:
        from_attributes = True
