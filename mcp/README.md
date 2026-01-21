# AI Todo Chatbot MCP Server

MCP Server providing task management tools for the AI Todo Chatbot.

## Tools

- `add_task` - Create a new task
- `list_tasks` - List tasks with optional status filter
- `complete_task` - Mark a task as completed
- `update_task` - Update task title/description
- `delete_task` - Delete a task

## Setup

1. Install dependencies:
```bash
pip install -e .
```

2. Copy `.env.example` to `.env` and set DATABASE_URL

3. Run the server:
```bash
python -m src.server
```
