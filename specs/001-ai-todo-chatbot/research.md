# Research: AI Todo Chatbot

**Feature**: 001-ai-todo-chatbot
**Date**: 2026-01-19
**Status**: Complete

## Technology Decisions

### 1. OpenAI Agents SDK Integration (with Gemini Backend)

**Decision**: Use OpenAI Agents SDK with Gemini API as the LLM backend via OpenAI-compatible endpoint.

**Rationale**:
- OpenAI Agents SDK provides excellent tool-use patterns
- Gemini API offers cost-effective, high-quality responses
- OpenAI-compatible endpoint allows seamless integration
- Built-in conversation context management

**CRITICAL Configuration** (MUST be at start of agent code):
```python
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
import os
from openai import AsyncOpenAI

load_dotenv()
set_tracing_disabled(True)

# Gemini API via OpenAI-compatible endpoint
provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=provider
)
```

**Environment Variable**: `GEMINI_API_KEY` (NOT OPENAI_API_KEY)

**Model**: `gemini-2.0-flash-exp`

**Alternatives Considered**:
- Direct OpenAI API: More expensive
- LangChain: More complex, heavier dependency footprint
- Anthropic Claude: Different SDK patterns

### 2. FastMCP Server Implementation

**Decision**: Use FastMCP to implement the 5 authorized MCP tools as a local server.

**Rationale**:
- Python-native MCP implementation
- Easy integration with FastAPI
- Structured input/output validation via Pydantic
- Constitution mandates MCP-only data access

**Alternatives Considered**:
- Custom tool implementation: Would bypass MCP abstraction layer
- External MCP server: Adds network latency and deployment complexity

**Tool Signatures**:
```python
@mcp.tool()
def add_task(user_id: str, title: str, description: str | None = None) -> dict:
    """Create a new task for the user."""

@mcp.tool()
def list_tasks(user_id: str, status: str | None = None) -> list[dict]:
    """List user's tasks, optionally filtered by status."""

@mcp.tool()
def update_task(user_id: str, task_id: int, title: str | None = None, description: str | None = None) -> dict:
    """Update an existing task's title or description."""

@mcp.tool()
def complete_task(user_id: str, task_id: int) -> dict:
    """Mark a task as completed."""

@mcp.tool()
def delete_task(user_id: str, task_id: int) -> dict:
    """Permanently delete a task."""
```

### 3. Database Strategy

**Decision**: SQLAlchemy ORM with SQLite for development, PostgreSQL for production.

**Rationale**:
- SQLAlchemy provides database-agnostic ORM
- SQLite requires zero configuration for local dev
- PostgreSQL offers production-grade reliability
- Alembic for schema migrations

**Alternatives Considered**:
- Raw SQL: Less maintainable, more error-prone
- MongoDB: Overkill for structured todo data
- Prisma: Python support less mature

**Connection Pattern**:
```python
# Stateless: Create session per request
async def get_db():
    async with AsyncSession(engine) as session:
        yield session
```

### 4. Conversation Context Management

**Decision**: Store conversation history in database, load last N messages per request.

**Rationale**:
- Constitution requires stateless backend
- DB storage enables crash recovery
- Configurable context window (default: 10 messages)
- User can start fresh by clearing conversation

**Alternatives Considered**:
- Redis cache: Adds infrastructure, not stateless
- In-memory: Violates constitution principle II
- No context: Poor user experience for multi-turn

**Context Loading**:
```python
async def get_conversation_context(user_id: str, limit: int = 10) -> list[Message]:
    """Load recent messages for agent context."""
    return await db.query(Message).filter_by(user_id=user_id).order_by(Message.created_at.desc()).limit(limit).all()
```

### 5. Chat Endpoint Design

**Decision**: Single `POST /api/{user_id}/chat` endpoint with JSON request/response.

**Rationale**:
- Constitution principle IV mandates single endpoint
- user_id in path for easy routing/logging
- JSON body for message content
- Response includes conversation_id, response, tool_calls

**Request/Response**:
```json
// Request
POST /api/user123/chat
{
    "message": "Add a task to buy groceries"
}

// Response
{
    "conversation_id": "conv_abc123",
    "response": "I've added 'buy groceries' to your tasks. Task ID: 42",
    "tool_calls": [
        {
            "tool": "add_task",
            "input": {"user_id": "user123", "title": "buy groceries"},
            "output": {"task_id": 42, "status": "pending", "title": "buy groceries"}
        }
    ]
}
```

### 6. Frontend Integration

**Decision**: ChatKit React component connected to chat endpoint.

**Rationale**:
- Constitution specifies ChatKit for UI
- React-based, easy to customize
- Handles message rendering, loading states
- Minimal frontend logic per principle V

**Alternatives Considered**:
- Custom chat UI: More work, same result
- Vercel AI SDK: Different paradigm, less control

## Best Practices Applied

### Error Handling

- All MCP tools return structured errors with user-friendly messages
- FastAPI exception handlers convert errors to JSON responses
- Agent receives error context to explain failures to users

### Logging

- Structured JSON logging for all operations
- Request ID tracking across layers
- Tool call logging for debugging agent behavior

### Security Considerations

- user_id scoping on all database queries
- Input validation via Pydantic models
- No secrets in logs or responses
- Rate limiting recommended for production

## Open Questions Resolved

| Question | Resolution |
|----------|------------|
| How to handle ambiguous user input? | Agent asks clarifying questions |
| Maximum context window size? | 10 messages default, configurable |
| Task ID format? | Auto-increment integer |
| How to match tasks by description? | Fuzzy search on title field |
| Concurrent request handling? | Async handlers, DB connection pooling |

## Dependencies

```txt
# Backend
fastapi>=0.109.0
uvicorn>=0.27.0
openai>=1.12.0
openai-agents>=0.1.0
sqlmodel>=0.0.14
alembic>=1.13.0
pydantic>=2.6.0
python-dotenv>=1.0.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
asyncpg>=0.29.0          # For Neon PostgreSQL async support
better-auth>=0.1.0       # Authentication

# MCP Server
mcp>=1.0.0               # Official MCP SDK

# Frontend
@chatkit/react
typescript
vite
```

## Environment Variables

```bash
# .env file
GEMINI_API_KEY=your-gemini-api-key    # NOT OPENAI_API_KEY
DATABASE_URL=postgresql+asyncpg://user:pass@host/db  # Neon PostgreSQL
```
