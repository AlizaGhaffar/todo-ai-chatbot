"""
Add Task MCP Tool

Creates a new task for a user.
"""

import logging
from datetime import datetime
from typing import Optional

from sqlmodel import select

from ..db import get_db_session
from ..models import Task

logger = logging.getLogger(__name__)


async def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None
) -> dict:
    """
    Add a new task for the user.

    Args:
        user_id: The user's ID
        title: Task title (1-200 chars)
        description: Optional task description (max 1000 chars)

    Returns:
        dict with task_id, status, title, description
    """
    # Validate inputs
    if not user_id or not user_id.strip():
        return {"error": "user_id is required"}

    if not title or not title.strip():
        return {"error": "title is required"}

    title = title.strip()[:200]
    if description:
        description = description.strip()[:1000]

    logger.info(f"Adding task for user {user_id}: {title}")

    session = await get_db_session()
    try:
        # Create new task
        task = Task(
            user_id=user_id.strip(),
            title=title,
            description=description,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        session.add(task)
        await session.commit()
        await session.refresh(task)

        logger.info(f"Task created with ID {task.id}")

        return {
            "task_id": task.id,
            "status": "pending",
            "title": task.title,
            "description": task.description,
            "message": f"Task '{task.title}' has been added successfully."
        }

    except Exception as e:
        await session.rollback()
        logger.error(f"Error adding task: {e}")
        return {"error": str(e)}

    finally:
        await session.close()
