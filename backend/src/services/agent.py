"""
AI Agent Service

Integrates OpenAI Agents SDK with MCP tools for task management.
"""

import logging
import json
from typing import Any, Optional

from agents import Agent, Runner, function_tool
from sqlmodel.ext.asyncio.session import AsyncSession

from .agent_config import get_agent_model, AGENT_CONFIG
from .agent_prompt import SYSTEM_PROMPT
from src.db.database import async_session_maker
from src.models import Task

logger = logging.getLogger(__name__)


# Tool implementations that will be registered with the agent
@function_tool
async def add_task(user_id: str, title: str, description: str = "") -> str:
    """
    Add a new task for the user.

    Args:
        user_id: The user's ID
        title: Task title (1-200 chars)
        description: Optional task description
    """
    from datetime import datetime

    logger.info(f"add_task called: user={user_id}, title={title}")

    async with async_session_maker() as session:
        try:
            task = Task(
                user_id=user_id,
                title=title[:200],
                description=description[:1000] if description else None,
                completed=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)

            return json.dumps({
                "task_id": task.id,
                "title": task.title,
                "status": "pending",
                "message": f"Task '{task.title}' has been added successfully."
            })
        except Exception as e:
            logger.error(f"Error adding task: {e}")
            return json.dumps({"error": str(e)})


@function_tool
async def list_tasks(user_id: str, status: str = "all") -> str:
    """
    List tasks for a user, optionally filtered by status.

    Args:
        user_id: The user's ID
        status: Filter - "all", "pending", or "completed"
    """
    from sqlmodel import select

    logger.info(f"list_tasks called: user={user_id}, status={status}")

    async with async_session_maker() as session:
        try:
            query = select(Task).where(Task.user_id == user_id)

            if status == "pending":
                query = query.where(Task.completed == False)
            elif status == "completed":
                query = query.where(Task.completed == True)

            query = query.order_by(Task.created_at.desc())

            result = await session.execute(query)
            tasks = result.scalars().all()

            task_list = [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "status": "completed" if t.completed else "pending",
                }
                for t in tasks
            ]

            return json.dumps({
                "tasks": task_list,
                "count": len(task_list),
                "message": f"Found {len(task_list)} task(s)."
            })
        except Exception as e:
            logger.error(f"Error listing tasks: {e}")
            return json.dumps({"error": str(e)})


@function_tool
async def complete_task(user_id: str, task_id: int) -> str:
    """
    Mark a task as completed by ID.

    Args:
        user_id: The user's ID
        task_id: The task ID to complete
    """
    from datetime import datetime
    from sqlmodel import select

    logger.info(f"complete_task called: user={user_id}, task_id={task_id}")

    async with async_session_maker() as session:
        try:
            query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await session.execute(query)
            task = result.scalar_one_or_none()

            if not task:
                return json.dumps({
                    "error": f"Task {task_id} not found",
                    "message": f"Could not find task with ID {task_id}."
                })

            task.completed = True
            task.updated_at = datetime.utcnow()
            session.add(task)
            await session.commit()

            return json.dumps({
                "task_id": task.id,
                "title": task.title,
                "status": "completed",
                "message": f"Task '{task.title}' has been marked as complete!"
            })
        except Exception as e:
            logger.error(f"Error completing task: {e}")
            return json.dumps({"error": str(e)})


@function_tool
async def complete_task_by_name(user_id: str, task_name: str) -> str:
    """
    Mark a task as completed by searching for its name/title. Use this when user refers to a task by name instead of ID.

    Args:
        user_id: The user's ID
        task_name: The task name/title to search for and complete
    """
    from datetime import datetime
    from sqlmodel import select

    logger.info(f"complete_task_by_name called: user={user_id}, task_name={task_name}")

    async with async_session_maker() as session:
        try:
            # Search for task by name (case-insensitive partial match)
            query = select(Task).where(
                Task.user_id == user_id,
                Task.completed == False
            )
            result = await session.execute(query)
            tasks = result.scalars().all()

            # Find matching task
            matching_task = None
            task_name_lower = task_name.lower()
            for task in tasks:
                if task_name_lower in task.title.lower() or task.title.lower() in task_name_lower:
                    matching_task = task
                    break

            if not matching_task:
                return json.dumps({
                    "error": f"Task '{task_name}' not found",
                    "message": f"Could not find a pending task matching '{task_name}'. Use list_tasks to see available tasks."
                })

            matching_task.completed = True
            matching_task.updated_at = datetime.utcnow()
            session.add(matching_task)
            await session.commit()

            return json.dumps({
                "task_id": matching_task.id,
                "title": matching_task.title,
                "status": "completed",
                "message": f"Task '{matching_task.title}' has been marked as complete!"
            })
        except Exception as e:
            logger.error(f"Error completing task by name: {e}")
            return json.dumps({"error": str(e)})


@function_tool
async def update_task(user_id: str, task_id: int, title: str = "", description: str = "") -> str:
    """
    Update a task's title or description.

    Args:
        user_id: The user's ID
        task_id: The task ID to update
        title: New task title (optional)
        description: New task description (optional)
    """
    from datetime import datetime
    from sqlmodel import select

    logger.info(f"update_task called: user={user_id}, task_id={task_id}")

    async with async_session_maker() as session:
        try:
            query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await session.execute(query)
            task = result.scalar_one_or_none()

            if not task:
                return json.dumps({
                    "error": f"Task {task_id} not found",
                    "message": f"Could not find task with ID {task_id}."
                })

            if title:
                task.title = title[:200]
            if description:
                task.description = description[:1000]

            task.updated_at = datetime.utcnow()
            session.add(task)
            await session.commit()

            return json.dumps({
                "task_id": task.id,
                "title": task.title,
                "status": "completed" if task.completed else "pending",
                "message": f"Task '{task.title}' has been updated."
            })
        except Exception as e:
            logger.error(f"Error updating task: {e}")
            return json.dumps({"error": str(e)})


@function_tool
async def delete_task(user_id: str, task_id: int) -> str:
    """
    Permanently delete a task.

    Args:
        user_id: The user's ID
        task_id: The task ID to delete
    """
    from sqlmodel import select

    logger.info(f"delete_task called: user={user_id}, task_id={task_id}")

    async with async_session_maker() as session:
        try:
            query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await session.execute(query)
            task = result.scalar_one_or_none()

            if not task:
                return json.dumps({
                    "error": f"Task {task_id} not found",
                    "message": f"Could not find task with ID {task_id}."
                })

            task_title = task.title
            await session.delete(task)
            await session.commit()

            return json.dumps({
                "task_id": task_id,
                "title": task_title,
                "deleted": True,
                "message": f"Task '{task_title}' has been deleted."
            })
        except Exception as e:
            logger.error(f"Error deleting task: {e}")
            return json.dumps({"error": str(e)})


def create_agent(user_id: str) -> Agent:
    """
    Create an AI agent configured with task management tools.

    Args:
        user_id: User ID for context

    Returns:
        Configured Agent instance
    """
    # Include user_id in the system prompt
    system_prompt = f"{SYSTEM_PROMPT}\n\n## Current User\nuser_id: {user_id}"

    agent = Agent(
        name="TodoAssistant",
        instructions=system_prompt,
        model=get_agent_model(),
        tools=[add_task, list_tasks, complete_task, complete_task_by_name, update_task, delete_task],
    )

    return agent


async def process_chat_message(
    user_id: str,
    message: str,
    conversation_history: list[dict] = None
) -> dict:
    """
    Process a chat message through the AI agent.

    Args:
        user_id: User's ID
        message: User's message
        conversation_history: Previous messages for context

    Returns:
        dict with response content and tool calls
    """
    logger.info(f"Processing message for user {user_id}: {message[:50]}...")

    try:
        agent = create_agent(user_id)

        # Build input messages
        input_messages = conversation_history or []
        input_messages.append({"role": "user", "content": message})

        # Run the agent
        result = await Runner.run(agent, input_messages)

        # Extract response
        response_content = result.final_output if hasattr(result, 'final_output') else str(result)

        # Extract tool calls if any
        tool_calls = []
        if hasattr(result, 'new_items'):
            for item in result.new_items:
                if hasattr(item, 'tool_calls') and item.tool_calls:
                    for tc in item.tool_calls:
                        tool_calls.append({
                            "tool": tc.name if hasattr(tc, 'name') else str(tc),
                            "input": tc.arguments if hasattr(tc, 'arguments') else {},
                        })

        logger.info(f"Agent response generated, tool_calls: {len(tool_calls)}")

        return {
            "content": response_content,
            "tool_calls": tool_calls if tool_calls else None,
        }

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        return {
            "content": "I encountered an error processing your request. Please try again.",
            "tool_calls": None,
            "error": str(e),
        }
