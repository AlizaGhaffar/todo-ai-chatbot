"""
Update Task MCP Tool

Updates a task's title or description.
"""

import logging
from datetime import datetime
from typing import Optional

from sqlmodel import select

from ..db import get_db_session
from ..models import Task

logger = logging.getLogger(__name__)


async def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    """
    Update a task's title or description.

    Args:
        user_id: The user's ID
        task_id: The task ID to update
        title: New task title (optional)
        description: New task description (optional)

    Returns:
        dict with updated task details
    """
    # Validate inputs
    if not user_id or not user_id.strip():
        return {"error": "user_id is required"}

    if not task_id or task_id < 1:
        return {"error": "valid task_id is required"}

    if not title and description is None:
        return {"error": "At least one of title or description must be provided"}

    user_id = user_id.strip()

    logger.info(f"Updating task {task_id} for user {user_id}")

    session = await get_db_session()
    try:
        # Find the task
        query = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            logger.warning(f"Task {task_id} not found for user {user_id}")
            return {
                "error": f"Task {task_id} not found",
                "message": f"Could not find task with ID {task_id}. Please check the task ID and try again."
            }

        # Track changes
        changes = []
        old_title = task.title

        # Update fields
        if title and title.strip():
            task.title = title.strip()[:200]
            changes.append(f"title changed from '{old_title}' to '{task.title}'")

        if description is not None:
            task.description = description.strip()[:1000] if description else None
            changes.append("description updated")

        task.updated_at = datetime.utcnow()

        session.add(task)
        await session.commit()
        await session.refresh(task)

        logger.info(f"Task {task_id} updated: {changes}")

        return {
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "status": "completed" if task.completed else "pending",
            "changes": changes,
            "message": f"Task '{task.title}' has been updated."
        }

    except Exception as e:
        await session.rollback()
        logger.error(f"Error updating task: {e}")
        return {"error": str(e)}

    finally:
        await session.close()
