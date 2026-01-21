# AI Todo Chatbot

An AI-powered Todo chatbot where users manage tasks via natural language. Built with OpenAI Agents SDK (using Gemini API backend) and MCP for task operations.

## Architecture

```
ChatKit (UI) → FastAPI (Backend) → OpenAI Agent → MCP Server → Neon PostgreSQL
```

## Quick Start

See [specs/001-ai-todo-chatbot/quickstart.md](specs/001-ai-todo-chatbot/quickstart.md) for setup instructions.

## Project Structure

```
backend/           # FastAPI server + Agent
├── src/
│   ├── api/       # FastAPI routes
│   ├── models/    # SQLModel models
│   ├── services/  # Agent and conversation logic
│   ├── auth/      # Better Auth configuration
│   └── db/        # Database connection and migrations
└── tests/

mcp/               # MCP Server (Official SDK)
├── src/
│   ├── server.py  # MCP server
│   └── tools/     # MCP tools (add, list, update, complete, delete)
└── tests/

frontend/          # ChatKit React UI
├── src/
│   ├── components/
│   └── services/
└── package.json
```

## Key Features

- Single chat endpoint: `POST /api/{user_id}/chat`
- 5 MCP tools: add_task, list_tasks, update_task, complete_task, delete_task
- Stateless backend with Neon PostgreSQL persistence
- Conversation context for natural multi-turn dialogue

## Environment Variables

```bash
# backend/.env
GEMINI_API_KEY=your-gemini-api-key
DATABASE_URL=postgresql+asyncpg://user:pass@host/db

# mcp/.env
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
```

## Constitution

This project follows principles defined in [.specify/memory/constitution.md](.specify/memory/constitution.md).
