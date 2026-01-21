# Data Model: AI Todo Chatbot

**Feature**: 001-ai-todo-chatbot
**Date**: 2026-01-19
**Status**: Complete

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                          User                                │
│  (external - not managed by this system)                    │
│  user_id: string (provided externally)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
┌─────────────────┐     ┌─────────────────────┐
│      Task       │     │    Conversation     │
├─────────────────┤     ├─────────────────────┤
│ id: int (PK)    │     │ id: string (PK)     │
│ user_id: string │     │ user_id: string     │
│ title: string   │     │ created_at: datetime│
│ description: str│     │ updated_at: datetime│
│ completed: bool │     └──────────┬──────────┘
│ created_at: dt  │                │
│ updated_at: dt  │                │ 1:N
└─────────────────┘                │
                                   ▼
                         ┌─────────────────────┐
                         │      Message        │
                         ├─────────────────────┤
                         │ id: string (PK)     │
                         │ user_id: string     │
                         │ conversation_id: FK │
                         │ role: enum          │
                         │ content: text       │
                         │ tool_calls: json    │
                         │ created_at: datetime│
                         └─────────────────────┘
```

## Entities

### Task

Represents a todo item belonging to a user.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | integer | PK, auto-increment | Unique task identifier |
| user_id | string(100) | NOT NULL, indexed | Owner's external user ID |
| title | string(200) | NOT NULL | Task title from user |
| description | text | NULL | Optional additional details |
| completed | boolean | NOT NULL, default: false | Completion status |
| created_at | datetime | NOT NULL, default: now | Creation timestamp |
| updated_at | datetime | NOT NULL, auto-update | Last modification timestamp |

**Indexes**:
- `idx_task_user_id` on (user_id)
- `idx_task_user_status` on (user_id, completed)

**Validation Rules**:
- title: 1-200 characters, trimmed
- description: 0-1000 characters (optional)
- user_id: required, non-empty

**State Transitions**:
```
pending (completed=false) ──complete_task──▶ completed (completed=true)
```

### Conversation

Represents a chat session for context continuity.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | string(36) | PK, UUID | Unique conversation identifier |
| user_id | string(100) | NOT NULL, indexed | Owner's external user ID |
| created_at | datetime | NOT NULL, default: now | Session start timestamp |
| updated_at | datetime | NOT NULL, auto-update | Last activity timestamp |

**Indexes**:
- `idx_conversation_user_id` on (user_id)

**Business Rules**:
- One active conversation per user at a time (latest by updated_at)
- New conversation created if none exists for user
- User can explicitly start fresh conversation

### Message

Represents a single message in a conversation.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | string(36) | PK, UUID | Unique message identifier |
| user_id | string(100) | NOT NULL | Owner's external user ID |
| conversation_id | string(36) | FK → Conversation.id | Parent conversation |
| role | enum | NOT NULL | 'user' or 'assistant' |
| content | text | NOT NULL | Message text content |
| tool_calls | json | NULL | MCP tool calls made (assistant only) |
| created_at | datetime | NOT NULL, default: now | Message timestamp |

**Indexes**:
- `idx_message_conversation` on (conversation_id, created_at)
- `idx_message_user` on (user_id, created_at)

**Role Enum Values**:
- `user`: Message from the user
- `assistant`: Response from the AI agent

**Tool Calls Schema** (JSON):
```json
[
    {
        "tool": "add_task",
        "input": {"user_id": "...", "title": "..."},
        "output": {"task_id": 42, "status": "pending", "title": "..."}
    }
]
```

## Database Migrations

### Initial Migration (001_initial_schema)

```sql
-- Create tasks table
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(100) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_task_user_id ON tasks(user_id);
CREATE INDEX idx_task_user_status ON tasks(user_id, completed);

-- Create conversations table
CREATE TABLE conversations (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversation_user_id ON conversations(user_id);

-- Create messages table
CREATE TABLE messages (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    conversation_id VARCHAR(36) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    tool_calls JSON,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

CREATE INDEX idx_message_conversation ON messages(conversation_id, created_at);
CREATE INDEX idx_message_user ON messages(user_id, created_at);
```

## Query Patterns

### Task Operations (MCP Tools)

```sql
-- add_task
INSERT INTO tasks (user_id, title, description, completed, created_at, updated_at)
VALUES (?, ?, ?, FALSE, NOW(), NOW())
RETURNING id, user_id, title, description, completed;

-- list_tasks (all)
SELECT id, title, description, completed, created_at
FROM tasks WHERE user_id = ? ORDER BY created_at DESC;

-- list_tasks (filtered by status)
SELECT id, title, description, completed, created_at
FROM tasks WHERE user_id = ? AND completed = ? ORDER BY created_at DESC;

-- update_task
UPDATE tasks SET title = COALESCE(?, title), description = COALESCE(?, description), updated_at = NOW()
WHERE id = ? AND user_id = ?
RETURNING id, title, description, completed;

-- complete_task
UPDATE tasks SET completed = TRUE, updated_at = NOW()
WHERE id = ? AND user_id = ?
RETURNING id, title, description, completed;

-- delete_task
DELETE FROM tasks WHERE id = ? AND user_id = ?
RETURNING id, title;
```

### Conversation Operations

```sql
-- Get or create conversation for user
INSERT INTO conversations (id, user_id, created_at, updated_at)
VALUES (?, ?, NOW(), NOW())
ON CONFLICT (id) DO UPDATE SET updated_at = NOW()
RETURNING id;

-- Get recent messages for context
SELECT id, role, content, tool_calls, created_at
FROM messages
WHERE conversation_id = ?
ORDER BY created_at DESC
LIMIT ?;

-- Save message
INSERT INTO messages (id, user_id, conversation_id, role, content, tool_calls, created_at)
VALUES (?, ?, ?, ?, ?, ?, NOW());
```

## Data Constraints Summary

| Entity | Constraint | Value |
|--------|-----------|-------|
| Task.title | max length | 200 chars |
| Task.description | max length | 1000 chars |
| Message.content | max length | 10000 chars |
| Conversation context | max messages | 10 (configurable) |
| user_id | max length | 100 chars |
