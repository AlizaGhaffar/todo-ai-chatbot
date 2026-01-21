"""
User Model

SQLModel User entity for authentication.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    """Base user fields."""
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=5, max_length=255, unique=True, index=True)


class User(UserBase, table=True):
    """User database model."""
    __tablename__ = "users"

    id: Optional[str] = Field(default=None, primary_key=True)
    password_hash: str = Field(..., max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=6, max_length=100)


class UserRead(UserBase):
    """Schema for reading user data."""
    id: str
    created_at: datetime
