---
description: "Task list for RAG Chatbot backend implementation"
---

# Tasks: RAG Chatbot Backend Setup and Core API Implementation

**Input**: Design documents from `/specs/1-rag-chatbot-backend/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Basic tests included per specification requirements.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Project structure**: `api/` as root, with `src/`, `tests/`, `scripts/` directories
- Adjust paths based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure in api/
- [X] T002 [P] Create directory structure: api/src/, api/scripts/, api/tests/
- [X] T003 [P] Add empty __init__.py files to all Python directories
- [X] T004 Create .python-version file with "3.11"
- [X] T005 Initialize uv project in api/ directory

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 [P] Add dependencies to pyproject.toml: fastapi, uvicorn, fastembed, agents, qdrant-client, pydantic, pydantic-settings, python-dotenv, sse-starlette, tiktoken, httpx
- [X] T007 [P] Add dev dependencies to pyproject.toml: pytest, pytest-asyncio
- [X] T008 Run uv sync to install all dependencies
- [X] T009 Create .env.example with GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY placeholders
- [X] T010 Create base configuration structure in api/src/config/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Backend API Setup (Priority: P1) 🎯 MVP

**Goal**: A developer can set up a robust backend API that can handle chat requests and respond with streaming responses. The system should be configured with all necessary dependencies and be ready to integrate with RAG functionality in future phases.

**Independent Test**: The backend can be started independently and responds to health checks. The /api/chat endpoint accepts messages and returns responses, demonstrating that all dependencies are properly installed and configured.

### Implementation for User Story 1

- [X] T011 [P] [US1] Implement settings.py with Pydantic Settings in api/src/config/settings.py
- [X] T012 [P] [US1] Create main.py with FastAPI app in api/src/main.py
- [X] T013 [P] [US1] Create routes directory structure in api/src/routes/
- [X] T014 [US1] Add CORS middleware configuration to main.py
- [X] T015 [US1] Implement GET /api/health endpoint in api/src/routes/health.py
- [X] T016 [US1] Create ChatRequest model in api/src/routes/chat.py
- [X] T017 [US1] Implement basic POST /api/chat endpoint in api/src/routes/chat.py
- [X] T018 [US1] Include health and chat routers in main.py
- [X] T019 [US1] Configure application startup on port 8000 with reload

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Streaming Chat Responses (Priority: P2)

**Goal**: A developer implements Server-Sent Events (SSE) for streaming chat responses to provide a better user experience with real-time responses.

**Independent Test**: The /api/chat endpoint can send responses as a stream using SSE, allowing clients to display responses as they are generated.

### Implementation for User Story 2

- [X] T020 [P] [US2] Update ChatRequest model to include optional selected_text and current_page fields in api/src/routes/chat.py
- [X] T021 [US2] Implement SSE streaming response in POST /api/chat endpoint in api/src/routes/chat.py
- [X] T022 [US2] Add streaming functionality to return chunk events in api/src/routes/chat.py
- [X] T023 [US2] Add sources event streaming to response in api/src/routes/chat.py
- [X] T024 [US2] Add done event to complete streaming in api/src/routes/chat.py
- [X] T025 [US2] Test streaming response functionality with placeholder content

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - External Service Integration (Priority: P3)

**Goal**: A developer connects the backend to external services including Qdrant for vector storage and Gemini for AI processing.

**Independent Test**: The backend can establish connections to Qdrant and Gemini services using provided credentials.

### Implementation for User Story 3

- [X] T026 [P] [US3] Create Qdrant service integration in api/src/services/qdrant_service.py
- [X] T027 [P] [US3] Create Gemini service integration in api/src/services/gemini_service.py
- [X] T028 [US3] Update chat endpoint to use Qdrant service for vector search in api/src/routes/chat.py
- [X] T029 [US3] Update chat endpoint to use Gemini service for AI responses in api/src/routes/chat.py
- [X] T030 [US3] Implement connection validation for external services
- [X] T031 [US3] Add error handling for external service unavailability

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Testing & Validation

**Purpose**: Add tests and validate all functionality

- [X] T032 [P] Create basic health endpoint test in api/tests/test_health.py
- [X] T033 [P] Create basic chat endpoint test in api/tests/test_chat.py
- [X] T034 Create integration test for complete chat flow in api/tests/test_integration.py
- [X] T035 Run all tests to verify functionality
- [X] T036 Test application startup and health check response
- [X] T037 Validate streaming response format and events

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T038 [P] Add logging configuration in api/src/main.py
- [X] T039 Add error handling middleware in api/src/main.py
- [X] T040 Update documentation in api/README.md
- [X] T041 Run quickstart validation to ensure all works as expected
- [X] T042 Verify all requirements from spec.md are met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Testing & Validation (Phase 6)**: Depends on all desired user stories being complete
- **Polish (Phase 7)**: Depends on all previous phases

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds on US1/US2 but should be independently testable

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all parallel tasks for User Story 1 together:
Task: "Implement settings.py with Pydantic Settings in api/src/config/settings.py"
Task: "Create main.py with FastAPI app in api/src/main.py"
Task: "Create routes directory structure in api/src/routes/"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [US1/US2/US3] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests pass after implementation
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence