# AI Todo Chatbot Backend

FastAPI backend for the AI Todo Chatbot with OpenAI Agents SDK and Gemini API.

## Setup

1. Install dependencies:
```bash
pip install -e .
```

2. Copy `.env.example` to `.env` and set your values:
```bash
cp .env.example .env
```

3. Run migrations:
```bash
alembic upgrade head
```

4. Start the server:
```bash
uvicorn src.api.main:app --reload
```

## API Endpoints

- `GET /health` - Health check
- `POST /api/{user_id}/chat` - Send chat message
- `POST /api/{user_id}/chat/new` - Start new conversation
