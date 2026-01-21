"""
Delete Task MCP Tool

Permanently deletes a task.
"""

import logging

from sqlmodel import select

from ..db import get_db_session
from ..models import Task

logger = logging.getLogger(__name__)


async def delete_task(
    user_id: str,
    task_id: int
) -> dict:
    """
    Permanently delete a task.

    Args:
        user_id: The user's ID
        task_id: The task ID to delete

    Returns:
        dict with deletion confirmation
    """
    # Validate inputs
    if not user_id or not user_id.strip():
        return {"error": "user_id is required"}

    if not task_id or task_id < 1:
        return {"error": "valid task_id is required"}

    user_id = user_id.strip()

    logger.info(f"Deleting task {task_id} for user {user_id}")

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

        # Store info before deletion
        task_title = task.title

        # Delete the task
        await session.delete(task)
        await session.commit()

        logger.info(f"Task {task_id} deleted")

        return {
            "task_id": task_id,
            "title": task_title,
            "deleted": True,
            "message": f"Task '{task_title}' has been deleted."
        }

    except Exception as e:
        await session.rollback()
        logger.error(f"Error deleting task: {e}")
        return {"error": str(e)}

    finally:
        await session.close()
