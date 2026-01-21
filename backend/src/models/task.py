"""
Task Model

SQLModel representation of a todo task.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    """Base task fields for validation."""

    title: str = Field(max_length=200, min_length=1, description="Task title")
    description: Optional[str] = Field(
        default=None, max_length=1000, description="Optional task details"
    )


class Task(TaskBase, table=True):
    """Task database model."""

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(max_length=100, index=True, description="Owner's external user ID")
    completed: bool = Field(default=False, description="Task completion status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")


class TaskCreate(TaskBase):
    """Schema for creating a task."""

    pass


class TaskUpdate(SQLModel):
    """Schema for updating a task."""

    title: Optional[str] = Field(default=None, max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskResponse(TaskBase):
    """Schema for task API responses."""

    id: int
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
