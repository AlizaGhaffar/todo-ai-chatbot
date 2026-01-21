"""
MCP Server for AI Todo Chatbot

Implements Model Context Protocol server using the Official MCP SDK.
Exposes task management tools for the AI agent.
"""

import asyncio
import logging
import os
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from dotenv import load_dotenv

from .db import get_db_session

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create MCP server instance
server = Server("ai-todo-chatbot")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="add_task",
            description="Add a new task for the user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "Task title (1-200 chars)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description (max 1000 chars)"
                    }
                },
                "required": ["user_id", "title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="List tasks for a user, optionally filtered by status",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's ID"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter by task status (default: all)"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's ID"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The task ID to complete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="update_task",
            description="Update a task's title or description",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's ID"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The task ID to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New task title (optional)"
                    },
                    "description": {
                        "type": "string",
                        "description": "New task description (optional)"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a task",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user's ID"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The task ID to delete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    logger.info(f"Tool call: {name} with args: {arguments}")

    try:
        if name == "add_task":
            from .tools.add_task import add_task
            result = await add_task(**arguments)
        elif name == "list_tasks":
            from .tools.list_tasks import list_tasks
            result = await list_tasks(**arguments)
        elif name == "complete_task":
            from .tools.complete_task import complete_task
            result = await complete_task(**arguments)
        elif name == "update_task":
            from .tools.update_task import update_task
            result = await update_task(**arguments)
        elif name == "delete_task":
            from .tools.delete_task import delete_task
            result = await delete_task(**arguments)
        else:
            result = {"error": f"Unknown tool: {name}"}

        return [TextContent(type="text", text=str(result))]

    except Exception as e:
        logger.error(f"Tool error: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server."""
    logger.info("Starting AI Todo Chatbot MCP Server...")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
