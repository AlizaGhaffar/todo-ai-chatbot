"""
Complete Task MCP Tool

Marks a task as completed.
"""

import logging
from datetime import datetime

from sqlmodel import select

from ..db import get_db_session
from ..models import Task

logger = logging.getLogger(__name__)


async def complete_task(
    user_id: str,
    task_id: int
) -> dict:
    """
    Mark a task as completed.

    Args:
        user_id: The user's ID
        task_id: The task ID to complete

    Returns:
        dict with task details and completion status
    """
    # Validate inputs
    if not user_id or not user_id.strip():
        return {"error": "user_id is required"}

    if not task_id or task_id < 1:
        return {"error": "valid task_id is required"}

    user_id = user_id.strip()

    logger.info(f"Completing task {task_id} for user {user_id}")

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

        if task.completed:
            return {
                "task_id": task.id,
                "title": task.title,
                "status": "completed",
                "message": f"Task '{task.title}' is already completed."
            }

        # Mark as completed
        task.completed = True
        task.updated_at = datetime.utcnow()

        session.add(task)
        await session.commit()
        await session.refresh(task)

        logger.info(f"Task {task_id} marked as completed")

        return {
            "task_id": task.id,
            "title": task.title,
            "status": "completed",
            "message": f"Task '{task.title}' has been marked as complete!"
        }

    except Exception as e:
        await session.rollback()
        logger.error(f"Error completing task: {e}")
        return {"error": str(e)}

    finally:
        await session.close()
