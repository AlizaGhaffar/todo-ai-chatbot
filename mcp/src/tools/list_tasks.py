"""
List Tasks MCP Tool

Lists tasks for a user with optional status filter.
"""

import logging
from typing import Optional

from sqlmodel import select

from ..db import get_db_session
from ..models import Task

logger = logging.getLogger(__name__)


async def list_tasks(
    user_id: str,
    status: Optional[str] = "all"
) -> dict:
    """
    List tasks for a user, optionally filtered by status.

    Args:
        user_id: The user's ID
        status: Filter by status - "all", "pending", or "completed"

    Returns:
        dict with tasks list and count
    """
    # Validate inputs
    if not user_id or not user_id.strip():
        return {"error": "user_id is required"}

    user_id = user_id.strip()
    status = (status or "all").lower()

    if status not in ["all", "pending", "completed"]:
        status = "all"

    logger.info(f"Listing tasks for user {user_id} with status filter: {status}")

    session = await get_db_session()
    try:
        # Build query
        query = select(Task).where(Task.user_id == user_id)

        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        query = query.order_by(Task.created_at.desc())

        # Execute query
        result = await session.execute(query)
        tasks = result.scalars().all()

        # Format response
        task_list = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": "completed" if task.completed else "pending",
                "created_at": task.created_at.isoformat() if task.created_at else None,
            }
            for task in tasks
        ]

        logger.info(f"Found {len(task_list)} tasks")

        return {
            "tasks": task_list,
            "count": len(task_list),
            "filter": status,
            "message": f"Found {len(task_list)} {'task' if len(task_list) == 1 else 'tasks'}."
        }

    except Exception as e:
        logger.error(f"Error listing tasks: {e}")
        return {"error": str(e)}

    finally:
        await session.close()
