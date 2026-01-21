# Implementation Plan: AI Todo Chatbot

**Branch**: `001-ai-todo-chatbot` | **Date**: 2026-01-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ai-todo-chatbot/spec.md`

## Summary

Build an AI-powered Todo chatbot that allows users to manage tasks via natural language through a single chat endpoint. The system uses OpenAI Agents SDK for intent interpretation and reasoning, FastMCP for tool execution, and maintains a stateless backend architecture with all persistence in SQLite/PostgreSQL.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, FastMCP, SQLAlchemy, Pydantic
**Storage**: SQLite (development), PostgreSQL (production-ready)
**Testing**: pytest, pytest-asyncio
**Target Platform**: Linux server (containerized)
**Project Type**: Web application (backend API + frontend chat UI)
**Performance Goals**: <3s response time, 100 concurrent users
**Constraints**: Stateless backend, MCP-only data access, single chat endpoint
**Scale/Scope**: Single-tenant per user_id, English language only

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Agentic Workflow Only | PASS | Following Specify → Plan → Tasks → Implement |
| II. Stateless Backend | PASS | No in-memory state; all persistence in DB |
| III. MCP-Only Actions | PASS | Agent uses 5 MCP tools exclusively |
| IV. Single Chat Endpoint | PASS | Only `POST /api/{user_id}/chat` |
| V. Clear Layer Separation | PASS | ChatKit → FastAPI → Agent → MCP → DB |
| VI. Allowed MCP Tools | PASS | Using only: add_task, list_tasks, update_task, complete_task, delete_task |
| VII. Conversation Persistence | PASS | Messages stored in DB per user/conversation |

**Gate Result**: PASS - All constitution principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-todo-chatbot/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── openapi.yaml     # API contract
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py          # Task SQLAlchemy model
│   │   ├── conversation.py  # Conversation model
│   │   └── message.py       # Message model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent.py         # OpenAI Agent service
│   │   └── conversation.py  # Conversation management
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app
│   │   └── routes/
│   │       └── chat.py      # Chat endpoint
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── server.py        # FastMCP server
│   │   └── tools/
│   │       ├── __init__.py
│   │       ├── add_task.py
│   │       ├── list_tasks.py
│   │       ├── update_task.py
│   │       ├── complete_task.py
│   │       └── delete_task.py
│   └── db/
│       ├── __init__.py
│       ├── database.py      # DB connection
│       └── migrations/      # Alembic migrations
└── tests/
    ├── contract/
    │   └── test_mcp_tools.py
    ├── integration/
    │   ├── test_chat_endpoint.py
    │   └── test_agent_flow.py
    └── unit/
        └── test_models.py

frontend/
├── src/
│   ├── components/
│   │   └── Chat.tsx         # ChatKit integration
│   ├── services/
│   │   └── api.ts           # Chat API client
│   └── App.tsx
└── package.json
```

**Structure Decision**: Web application structure selected because the feature requires both a backend API (FastAPI + MCP) and a frontend chat interface (ChatKit). The backend contains all business logic layers (API, Agent, MCP, DB) while frontend is presentation-only per constitution.

## Complexity Tracking

> No violations - all constitution principles satisfied without exceptions.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Generated Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Research | [research.md](./research.md) | Complete |
| Data Model | [data-model.md](./data-model.md) | Complete |
| API Contract | [contracts/openapi.yaml](./contracts/openapi.yaml) | Complete |
| Quickstart | [quickstart.md](./quickstart.md) | Complete |
| Tasks | [tasks.md](./tasks.md) | Pending (`/sp.tasks`) |

## Next Steps

1. Run `/sp.tasks` to generate implementation task list
2. Follow tasks in dependency order
3. Run tests after each phase completion
