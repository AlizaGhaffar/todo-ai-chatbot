<!--
Sync Impact Report
==================
Version Change: 0.0.0 → 1.0.0 (MAJOR - initial constitution ratification)
Modified Principles: N/A (initial creation)
Added Sections:
  - Core Principles (7 principles)
  - Architecture & Layers
  - Development Workflow
  - Governance
Removed Sections: None
Templates Requiring Updates:
  - .specify/templates/plan-template.md ✅ (compatible - uses Constitution Check pattern)
  - .specify/templates/spec-template.md ✅ (compatible - uses standard spec format)
  - .specify/templates/tasks-template.md ✅ (compatible - uses phased task structure)
Follow-up TODOs: None
-->

# AI Todo Chatbot Constitution

## Core Principles

### I. Agentic Workflow Only

All development MUST follow the Specify → Plan → Tasks → Implement workflow.

**Non-Negotiable Rules:**
- Every feature starts with a specification (`/sp.specify`)
- Planning phase MUST precede implementation (`/sp.plan`)
- Tasks MUST be generated from plan artifacts (`/sp.tasks`)
- No manual logic shortcuts or ad-hoc implementation allowed
- Each phase requires explicit completion before proceeding

**Rationale:** Enforces disciplined, traceable development that prevents shortcuts and ensures all decisions are documented.

### II. Stateless Backend

The backend MUST NOT hold any in-memory state between requests.

**Non-Negotiable Rules:**
- All application state MUST be persisted in the database
- No global variables, caches, or session stores in memory
- Each request MUST be independently processable
- Server restarts MUST NOT lose any user data
- Horizontal scaling MUST be supported without state synchronization

**Rationale:** Enables horizontal scaling, crash recovery, and predictable behavior across all instances.

### III. MCP-Only Actions

AI agents MUST NOT access the database directly. All task operations MUST be executed via MCP tools only.

**Non-Negotiable Rules:**
- Agents interact exclusively through MCP tool interface
- Direct database queries from agent code are forbidden
- All data mutations flow through MCP server
- MCP tools return structured, typed responses
- Tool failures MUST be handled gracefully with clear error messages

**Rationale:** Creates a clean separation between AI reasoning and data operations, enabling auditing, rate limiting, and access control.

### IV. Single Chat Endpoint

Only one endpoint is allowed: `POST /api/{user_id}/chat`

**Non-Negotiable Rules:**
- No additional REST endpoints for task operations
- Agent decides which MCP tool(s) to call based on user intent
- User ID is the only path parameter required
- Request body contains only the user message
- Response contains agent's reply and any tool execution results

**Rationale:** Simplifies API surface, centralizes all user interactions, and lets the AI agent handle routing logic.

### V. Clear Layer Separation

System MUST maintain strict boundaries between architectural layers.

**Non-Negotiable Rules:**
- **ChatKit (UI):** Presentation only, no business logic
- **FastAPI (Backend):** Request orchestration and API handling only
- **Agent (OpenAI SDK):** Reasoning and tool selection only
- **MCP Server:** Task operation execution only
- **Database:** Single source of truth for all persistent data

**Rationale:** Enables independent testing, deployment, and evolution of each layer without coupling.

### VI. Allowed MCP Tools

Only the following MCP tools are permitted for task operations:

**Authorized Tools:**
- `add_task` - Create a new task for the user
- `list_tasks` - Retrieve user's tasks with optional filters
- `update_task` - Modify task title, description, or metadata
- `complete_task` - Mark a task as completed
- `delete_task` - Remove a task permanently

**Non-Negotiable Rules:**
- All tools MUST be stateless (no side effects beyond database)
- All tools MUST return structured JSON output
- All tools MUST validate input parameters
- All tools MUST include user_id scoping
- No additional tools without constitution amendment

**Rationale:** Defines a minimal, complete API surface that covers all todo operations while preventing scope creep.

### VII. Conversation Persistence

User conversations MUST be maintained for context continuity.

**Non-Negotiable Rules:**
- Conversation history MUST be stored per user
- Agent MUST have access to recent conversation context
- Context window MUST be managed to prevent token overflow
- Conversation data MUST be retrievable for debugging
- User MUST be able to start fresh conversations

**Rationale:** Enables natural multi-turn conversations and allows users to reference previous messages.

## Architecture & Layers

### System Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   ChatKit   │────▶│   FastAPI   │────▶│ OpenAI SDK  │
│    (UI)     │◀────│  (Backend)  │◀────│   (Agent)   │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
                    ┌─────────────┐     ┌─────────────┐
                    │  Database   │◀────│ MCP Server  │
                    │   (SQLite)  │     │  (Tools)    │
                    └─────────────┘     └─────────────┘
```

### Technology Stack

- **Frontend:** ChatKit (React-based chat UI)
- **Backend:** FastAPI (Python 3.11+)
- **Agent:** OpenAI Agents SDK
- **Tools:** FastMCP (MCP server implementation)
- **Database:** SQLite (development), PostgreSQL (production-ready)

### Data Flow

1. User sends message via ChatKit
2. FastAPI receives at `POST /api/{user_id}/chat`
3. FastAPI invokes OpenAI Agent with message + context
4. Agent reasons and selects appropriate MCP tool(s)
5. MCP Server executes tool against database
6. Results flow back through Agent → FastAPI → ChatKit

## Development Workflow

### Mandatory Process

1. **Specify** (`/sp.specify`): Define feature requirements and acceptance criteria
2. **Plan** (`/sp.plan`): Create technical architecture and design decisions
3. **Tasks** (`/sp.tasks`): Generate actionable, testable task list
4. **Implement**: Execute tasks following Red-Green-Refactor when applicable

### Code Quality Standards

- All code MUST pass linting (ruff for Python)
- All public functions MUST have type hints
- All MCP tools MUST have integration tests
- Error handling MUST be explicit, not silenced
- Logging MUST be structured (JSON format)

### Testing Requirements

- MCP tools require contract tests
- Agent behavior requires integration tests
- UI components require snapshot tests (optional)
- End-to-end tests for critical user journeys

## Governance

### Amendment Process

1. Propose change with rationale
2. Document impact on existing code
3. Update version following semver:
   - MAJOR: Breaking changes to principles
   - MINOR: New principles or sections
   - PATCH: Clarifications or typo fixes
4. Update dependent templates if affected

### Compliance

- All PRs MUST verify constitution compliance
- Architecture Decision Records (ADRs) for significant deviations
- Regular reviews during retrospectives

### Guidance

For runtime development guidance, refer to:
- `CLAUDE.md` - Agent-specific instructions
- `specs/*/plan.md` - Feature-specific architecture
- `history/adr/` - Past architectural decisions

**Version**: 1.0.0 | **Ratified**: 2026-01-19 | **Last Amended**: 2026-01-19
