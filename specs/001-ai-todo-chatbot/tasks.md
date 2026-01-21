# Tasks: AI Todo Chatbot

**Input**: Design documents from `/specs/001-ai-todo-chatbot/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/openapi.yaml, research.md, quickstart.md

**Tests**: Tests included as part of validation phase per user input.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`, `mcp/`
- Structure per plan.md with user-specified modifications (SQLModel, Better Auth, Neon PostgreSQL, Official MCP SDK)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure with /frontend, /backend, /mcp, /specs directories
- [ ] T002 [P] Initialize backend Python project with pyproject.toml in backend/
- [ ] T003 [P] Initialize frontend Node.js project with package.json in frontend/
- [ ] T004 [P] Initialize MCP server project with pyproject.toml in mcp/
- [ ] T005 Configure environment variables in backend/.env.example (GEMINI_API_KEY, DATABASE_URL) and mcp/.env.example (DATABASE_URL)
- [ ] T006 [P] Setup Better Auth configuration in backend/src/auth/config.py
- [ ] T007 Connect Neon PostgreSQL with connection string in backend/src/db/database.py

**Checkpoint**: Project structure ready, dependencies configured

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Database Layer

- [ ] T008 Create SQLModel Task model in backend/src/models/task.py
- [ ] T009 [P] Create SQLModel Conversation model in backend/src/models/conversation.py
- [ ] T010 [P] Create SQLModel Message model in backend/src/models/message.py
- [ ] T011 Create models __init__.py exporting all models in backend/src/models/__init__.py
- [ ] T012 Create DB migration scripts using Alembic in backend/src/db/migrations/
- [ ] T013 Verify DB connectivity with health check in backend/src/db/health.py

### MCP Server Foundation

- [ ] T014 Initialize MCP server using Official MCP SDK in mcp/src/server.py
- [ ] T015 [P] Create MCP tools __init__.py in mcp/src/tools/__init__.py
- [ ] T016 [P] Configure MCP server database connection in mcp/src/db.py

### API Foundation

- [ ] T017 Create FastAPI app with CORS in backend/src/api/main.py
- [ ] T018 [P] Setup API error handling middleware in backend/src/api/middleware/error_handler.py
- [ ] T019 [P] Setup structured logging in backend/src/api/middleware/logging.py

### Agent Foundation

- [ ] T020 Configure OpenAI Agents SDK with Gemini API backend in backend/src/services/agent_config.py (MUST use GEMINI_API_KEY, gemini-2.0-flash-exp model, Google's OpenAI-compatible endpoint)
- [ ] T021 Define agent system prompt and behavior rules in backend/src/services/agent_prompt.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add Task via Chat (Priority: P1)

**Goal**: Users can add new tasks by typing natural language messages like "Add a task to buy groceries"

**Independent Test**: Send chat message with add intent, verify task appears in database with correct attributes

### MCP Tool for US1

- [ ] T022 [US1] Implement add_task MCP tool in mcp/src/tools/add_task.py
- [ ] T023 [US1] Register add_task tool with MCP server in mcp/src/server.py

### Agent Integration for US1

- [ ] T024 [US1] Register add_task MCP tool with OpenAI agent in backend/src/services/agent.py
- [ ] T025 [US1] Add intent detection for "add" commands in agent prompt

### API for US1

- [ ] T026 [US1] Implement POST /api/{user_id}/chat endpoint in backend/src/api/routes/chat.py
- [ ] T027 [US1] Implement conversation service to fetch/save messages in backend/src/services/conversation.py
- [ ] T028 [US1] Wire chat endpoint to agent service in backend/src/api/routes/chat.py

**Checkpoint**: User Story 1 complete - can add tasks via natural language

---

## Phase 4: User Story 2 - List Tasks via Chat (Priority: P1)

**Goal**: Users can view their tasks by asking "Show my tasks" or "What's on my todo list"

**Independent Test**: Request task list, verify response contains all user's tasks with correct details

### MCP Tool for US2

- [ ] T029 [US2] Implement list_tasks MCP tool with status filter in mcp/src/tools/list_tasks.py
- [ ] T030 [US2] Register list_tasks tool with MCP server in mcp/src/server.py

### Agent Integration for US2

- [ ] T031 [US2] Register list_tasks MCP tool with agent in backend/src/services/agent.py
- [ ] T032 [US2] Add intent detection for "list/show" commands in agent prompt

**Checkpoint**: User Stories 1 & 2 complete - MVP functional (add + list)

---

## Phase 5: User Story 3 - Complete Task via Chat (Priority: P2)

**Goal**: Users can mark tasks complete by saying "Complete task 5" or "I finished buying groceries"

**Independent Test**: Complete a known task, verify status changes to completed

### MCP Tool for US3

- [ ] T033 [US3] Implement complete_task MCP tool in mcp/src/tools/complete_task.py
- [ ] T034 [US3] Register complete_task tool with MCP server in mcp/src/server.py

### Agent Integration for US3

- [ ] T035 [US3] Register complete_task MCP tool with agent in backend/src/services/agent.py
- [ ] T036 [US3] Add intent detection for "complete/finish/done" commands in agent prompt
- [ ] T037 [US3] Add task matching by title in agent for natural language completion

**Checkpoint**: User Story 3 complete - full task lifecycle (add → list → complete)

---

## Phase 6: User Story 4 - Update Task via Chat (Priority: P2)

**Goal**: Users can update task title/description by saying "Update task 3 to Review Q1 report"

**Independent Test**: Update a task, verify changes persist correctly

### MCP Tool for US4

- [ ] T038 [US4] Implement update_task MCP tool in mcp/src/tools/update_task.py
- [ ] T039 [US4] Register update_task tool with MCP server in mcp/src/server.py

### Agent Integration for US4

- [ ] T040 [US4] Register update_task MCP tool with agent in backend/src/services/agent.py
- [ ] T041 [US4] Add intent detection for "update/change/modify" commands in agent prompt

**Checkpoint**: User Story 4 complete - tasks can be modified

---

## Phase 7: User Story 5 - Delete Task via Chat (Priority: P3)

**Goal**: Users can delete tasks by saying "Delete task 7" or "Remove the grocery task"

**Independent Test**: Delete a task, verify it no longer appears in task list

### MCP Tool for US5

- [ ] T042 [US5] Implement delete_task MCP tool in mcp/src/tools/delete_task.py
- [ ] T043 [US5] Register delete_task tool with MCP server in mcp/src/server.py

### Agent Integration for US5

- [ ] T044 [US5] Register delete_task MCP tool with agent in backend/src/services/agent.py
- [ ] T045 [US5] Add intent detection for "delete/remove" commands in agent prompt

**Checkpoint**: User Story 5 complete - full CRUD operations available

---

## Phase 8: User Story 6 - Conversation Context (Priority: P3)

**Goal**: Chatbot remembers conversation context for references like "complete that one"

**Independent Test**: Multi-turn conversation with context references resolves correctly

### Implementation for US6

- [ ] T046 [US6] Implement context loading (last 10 messages) in backend/src/services/conversation.py
- [ ] T047 [US6] Pass conversation history to agent in backend/src/services/agent.py
- [ ] T048 [US6] Enable multi-tool chaining in agent for context-aware responses

**Checkpoint**: User Story 6 complete - natural multi-turn conversations supported

---

## Phase 9: Frontend (ChatKit Integration)

**Purpose**: Connect ChatKit UI to chat endpoint

- [ ] T049 Setup ChatKit React component in frontend/src/components/Chat.tsx
- [ ] T050 [P] Create API client service in frontend/src/services/api.ts
- [ ] T051 Connect ChatKit to POST /api/{user_id}/chat endpoint in frontend/src/components/Chat.tsx
- [ ] T052 [P] Render assistant responses and tool call confirmations in frontend/src/components/Chat.tsx
- [ ] T053 [P] Handle loading states during API calls in frontend/src/components/Chat.tsx
- [ ] T054 [P] Handle error states with user-friendly messages in frontend/src/components/Chat.tsx
- [ ] T055 Create main App component integrating Chat in frontend/src/App.tsx

**Checkpoint**: Frontend complete - full user interface ready

---

## Phase 10: Testing & Validation

**Purpose**: Verify all functionality works correctly

- [ ] T056 [P] Test add task natural language command (manual or automated)
- [ ] T057 [P] Test list tasks with status filter
- [ ] T058 [P] Test complete task by ID and by description
- [ ] T059 [P] Test update task title and description
- [ ] T060 [P] Test delete task
- [ ] T061 Verify stateless behavior - restart server, verify no data loss
- [ ] T062 Test conversation context with multi-turn dialogue
- [ ] T063 Validate error handling for invalid inputs and non-existent tasks
- [ ] T064 Validate all MCP tool schemas match contracts/openapi.yaml

**Checkpoint**: All tests pass - ready for deployment

---

## Phase 11: Deployment

**Purpose**: Deploy application to production

- [ ] T065 Deploy MCP server (containerized or serverless)
- [ ] T066 [P] Deploy backend FastAPI server
- [ ] T067 [P] Deploy frontend to CDN/static hosting
- [ ] T068 Configure ChatKit domain allowlist for production
- [ ] T069 Run final end-to-end verification in production environment
- [ ] T070 Run quickstart.md validation to ensure documentation accuracy

**Checkpoint**: Application deployed and verified

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - US1 (Add) and US2 (List) can run in parallel after Foundation
  - US3-6 can start after Foundation (independent of each other)
- **Frontend (Phase 9)**: Depends on at least US1 + US2 for basic demo
- **Testing (Phase 10)**: Depends on all user stories complete
- **Deployment (Phase 11)**: Depends on Testing phase completion

### User Story Dependencies

| Story | Priority | Depends On | Can Parallel With |
|-------|----------|------------|-------------------|
| US1 - Add Task | P1 | Foundation | US2, US3, US4, US5, US6 |
| US2 - List Tasks | P1 | Foundation | US1, US3, US4, US5, US6 |
| US3 - Complete Task | P2 | Foundation | US1, US2, US4, US5, US6 |
| US4 - Update Task | P2 | Foundation | US1, US2, US3, US5, US6 |
| US5 - Delete Task | P3 | Foundation | US1, US2, US3, US4, US6 |
| US6 - Context | P3 | Foundation | US1, US2, US3, US4, US5 |

### Within Each User Story

1. MCP tool implementation first
2. Register tool with MCP server
3. Register tool with agent
4. Update agent prompt for intent detection

### Parallel Opportunities

```bash
# Phase 1 parallel tasks:
T002, T003, T004  # Initialize projects in parallel

# Phase 2 parallel tasks:
T009, T010        # Conversation and Message models
T015, T016        # MCP tools init and DB config
T018, T019        # Error handler and logging middleware

# All user stories can run in parallel after Phase 2

# Phase 9 parallel tasks:
T052, T053, T054  # ChatKit rendering, loading, errors

# Phase 10 parallel tasks:
T056-T060         # All functional tests
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: US1 - Add Task
4. Complete Phase 4: US2 - List Tasks
5. **STOP and VALIDATE**: Test add + list independently
6. Deploy MVP if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 + US2 → MVP! (add + list)
3. US3 → Complete task lifecycle
4. US4 → Task refinement
5. US5 → Cleanup capability
6. US6 → Enhanced UX with context
7. Frontend → Full user interface
8. Testing → Quality assurance
9. Deployment → Production ready

---

## Task Summary

| Phase | Task Count | Parallel Tasks |
|-------|------------|----------------|
| Phase 1: Setup | 7 | 4 |
| Phase 2: Foundation | 14 | 6 |
| Phase 3: US1 Add | 7 | 0 |
| Phase 4: US2 List | 4 | 0 |
| Phase 5: US3 Complete | 5 | 0 |
| Phase 6: US4 Update | 4 | 0 |
| Phase 7: US5 Delete | 4 | 0 |
| Phase 8: US6 Context | 3 | 0 |
| Phase 9: Frontend | 7 | 4 |
| Phase 10: Testing | 9 | 5 |
| Phase 11: Deployment | 6 | 2 |
| **Total** | **70** | **21** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- User specified SQLModel (not SQLAlchemy), Better Auth, Neon PostgreSQL, Official MCP SDK
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
