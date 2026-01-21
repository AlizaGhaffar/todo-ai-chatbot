---
id: 001
title: AI Todo Chatbot Constitution Ratified
stage: constitution
date: 2026-01-19
surface: agent
model: claude-opus-4-5
feature: none
branch: master
user: affil
command: /sp.constitution
labels: ["constitution", "governance", "principles", "openai-agents-sdk", "mcp", "fastapi"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (constitution document)
---

## Prompt

Project:
AI-based Todo Chatbot using OpenAI Agents SDK and MCP

Goal:
Allow users to manage todos via natural language chat using an agentic,
stateless architecture.

Non-Negotiable Rules:

1. Agentic Workflow Only
- Follow: Specify → Plan → Tasks → Implement
- No manual logic or shortcuts.

2. Stateless Backend
- Backend holds no in-memory state.
- All state is stored in the database.

3. MCP-Only Actions
- AI agents must NOT access the database directly.
- All task operations must be executed via MCP tools only.

4. Single Chat Endpoint
- Only one endpoint is allowed:
  POST /api/{user_id}/chat
- Agent decides which MCP tool(s) to call.

5. Clear Layer Separation
- ChatKit: UI only
- FastAPI: request orchestration
- Agent (OpenAI SDK): reasoning + tool selection
- MCP Server: execute task operations
- Database: single source of truth

6. Allowed MCP Tools
- add_task
- list_tasks
- update_task
- complete_task
- delete_task
(All tools must be stateless and return structured output.)

7. Conversation Persistence (inferred from context)

## Response snapshot

Created constitution v1.0.0 for AI Todo Chatbot project with 7 core principles:

1. **Agentic Workflow Only** - Mandatory Specify → Plan → Tasks → Implement flow
2. **Stateless Backend** - No in-memory state, all persistence in database
3. **MCP-Only Actions** - Agents use MCP tools exclusively, no direct DB access
4. **Single Chat Endpoint** - Only `POST /api/{user_id}/chat` allowed
5. **Clear Layer Separation** - ChatKit → FastAPI → Agent → MCP → Database
6. **Allowed MCP Tools** - add_task, list_tasks, update_task, complete_task, delete_task
7. **Conversation Persistence** - User conversations maintained for context

Architecture diagram and technology stack (FastAPI, OpenAI Agents SDK, FastMCP, SQLite/PostgreSQL) documented. Development workflow and governance rules established.

## Outcome

- Impact: Initial constitution ratified establishing project governance
- Tests: N/A (governance document)
- Files: `.specify/memory/constitution.md` created
- Next prompts: `/sp.specify` for first feature, then `/sp.plan` and `/sp.tasks`
- Reflection: User provided clear principles; 7th principle (Conversation Persistence) was incomplete in input but inferred from context

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - all placeholders filled, version set, templates validated
- Prompt variant (if applicable): N/A
- Next experiment: N/A
