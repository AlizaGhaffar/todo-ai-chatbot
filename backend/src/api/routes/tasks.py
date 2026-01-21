"""
Tasks API Routes

Handles task listing and management via REST API.
"""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.db.database import get_session
from src.auth.config import get_current_user_id
from src.models import Task, TaskResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def list_tasks(
    user_id: str,
    status: str = None,
    session: AsyncSession = Depends(get_session),
):
    """
    List all tasks for a user.

    Args:
        user_id: User identifier
        status: Optional filter by status ('pending' or 'completed')

    Returns:
        List of tasks for the user
    """
    validated_user_id = get_current_user_id(user_id)

    logger.info(f"Fetching tasks for user {validated_user_id}")

    # Build query
    query = select(Task).where(Task.user_id == validated_user_id)

    # Apply status filter if provided
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)

    # Order by created_at descending (newest first)
    query = query.order_by(Task.created_at.desc())

    result = await session.exec(query)
    tasks = result.all()

    logger.info(f"Found {len(tasks)} tasks for user {validated_user_id}")

    return [
        TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
        for task in tasks
    ]
