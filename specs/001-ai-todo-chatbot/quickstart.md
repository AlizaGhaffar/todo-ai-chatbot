# Quickstart: AI Todo Chatbot

**Feature**: 001-ai-todo-chatbot
**Date**: 2026-01-19

## Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- Gemini API key (from Google AI Studio)
- Neon PostgreSQL database

## Quick Setup

### 1. Clone and Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GEMINI_API_KEY=your-gemini-api-key
DATABASE_URL=postgresql+asyncpg://user:pass@your-neon-host/dbname
EOF

# Run database migrations
alembic upgrade head

# Start the server
uvicorn src.api.main:app --reload --port 8000
```

### 2. Setup MCP Server

```bash
cd mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (same DB connection)
cat > .env << EOF
DATABASE_URL=postgresql+asyncpg://user:pass@your-neon-host/dbname
EOF

# Start MCP server
python -m src.server
```

### 3. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env

# Start development server
npm run dev
```

### 4. Test the API

```bash
# Add a task
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'

# List tasks
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show my tasks"}'

# Complete a task
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Complete task 1"}'
```

## Project Structure

```
backend/
├── src/
│   ├── api/           # FastAPI application
│   ├── models/        # SQLModel models
│   ├── services/      # Agent and conversation logic
│   ├── auth/          # Better Auth configuration
│   └── db/            # Database configuration
└── tests/             # Test suites

mcp/
├── src/
│   ├── server.py      # MCP server (Official SDK)
│   ├── tools/         # MCP tools (add, list, update, complete, delete)
│   └── db.py          # Database connection
└── tests/

frontend/
├── src/
│   ├── components/    # React components (ChatKit)
│   └── services/      # API client
└── package.json
```

## Key Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/{user_id}/chat` | Send chat message, get AI response |

## Environment Variables

### Backend

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Gemini API key for agent (NOT OpenAI) | Yes |
| `DATABASE_URL` | Neon PostgreSQL connection string | Yes |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING) | No |

### MCP Server

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | Neon PostgreSQL connection string | Yes |

### Frontend

| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_API_URL` | Backend API URL | Yes |

## Agent Configuration (CRITICAL)

The agent MUST be configured with Gemini API at the start of `backend/src/services/agent.py`:

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

## Running Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/integration/test_chat_endpoint.py -v
```

## Common Issues

### "GEMINI_API_KEY not set"
Ensure your `.env` file contains a valid Gemini API key from Google AI Studio.

### "Database connection failed"
- Verify your Neon PostgreSQL connection string is correct
- Check that the database exists and is accessible
- Ensure asyncpg is installed: `pip install asyncpg`

### "Connection refused" on frontend
Check that the backend is running on port 8000.

### "MCP tools not found"
Ensure the MCP server is running and accessible from the backend.

## Next Steps

1. Follow tasks.md to implement each component
2. Start with Phase 1 (Setup) and Phase 2 (Foundation)
3. Test after each user story completion
