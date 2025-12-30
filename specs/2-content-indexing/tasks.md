---
description: "Task list for RAG Chatbot content indexing implementation"
---

# Tasks: RAG Chatbot Part 2: Content Indexing and RAG Service

**Input**: Design documents from `/specs/2-content-indexing/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Basic tests included per specification requirements.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Project structure**: `api/` as root, with `src/`, `scripts/`, `docs/` directories
- Adjust paths based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create directory structure for services in api/src/services/
- [ ] T002 [P] Create utils directory in api/src/services/utils/
- [ ] T003 [P] Add empty __init__.py files to all Python directories
- [ ] T004 Create scripts directory in api/scripts/
- [ ] T005 [P] Add empty __init__.py files to scripts directories

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 [P] Add fastembed dependency to pyproject.toml
- [ ] T007 [P] Add tiktoken dependency to pyproject.toml
- [ ] T008 Run uv sync to install new dependencies
- [ ] T009 Verify Qdrant connection with existing credentials
- [ ] T010 Create docs directory structure with sample markdown files

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Content Indexing (Priority: P1) 🎯 MVP

**Goal**: A developer can index textbook content into a vector database so that the RAG chatbot can retrieve relevant information. The system should process markdown files and store them with proper metadata for later retrieval.

**Independent Test**: The indexing script processes markdown files and stores them in Qdrant with preserved metadata. The system can verify that content has been properly indexed.

### Implementation for User Story 1

- [ ] T011 [P] [US1] Create chunker utility in api/src/services/utils/chunker.py
- [ ] T012 [US1] Implement markdown loading and heading-based splitting in api/src/services/utils/chunker.py
- [ ] T013 [US1] Add token counting with tiktoken in api/src/services/utils/chunker.py
- [ ] T014 [US1] Implement chunk size limits and overlap in api/src/services/utils/chunker.py
- [ ] T015 [US1] Extract and preserve metadata in api/src/services/utils/chunker.py
- [ ] T016 [P] [US1] Create embeddings service in api/src/services/embeddings.py
- [ ] T017 [US1] Implement embed_texts function with FastEmbed in api/src/services/embeddings.py
- [ ] T018 [US1] Verify 384-dimensional vector output in api/src/services/embeddings.py
- [ ] T019 [US1] Create indexer script in api/scripts/index_content.py
- [ ] T020 [US1] Define Phase 1 file paths in api/scripts/index_content.py
- [ ] T021 [US1] Integrate chunking and embedding services in api/scripts/index_content.py
- [ ] T022 [US1] Connect to Qdrant Cloud using existing settings in api/scripts/index_content.py
- [ ] T023 [US1] Create collection if not exists with proper schema in api/scripts/index_content.py
- [ ] T024 [US1] Upsert chunks with metadata in api/scripts/index_content.py
- [ ] T025 [US1] Add progress reporting to indexer script in api/scripts/index_content.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Content Chunking (Priority: P2)

**Goal**: A developer can split large documents into smaller chunks that maintain context while being suitable for embedding and retrieval. The system should follow specific chunking rules to optimize for search quality.

**Independent Test**: The system can take a large markdown document and split it according to the specified rules: by ## headings, max 1000 tokens, with 100-token overlap.

### Implementation for User Story 2

- [ ] T026 [US2] Enhance chunking logic for proper heading detection in api/src/services/utils/chunker.py
- [ ] T027 [US2] Implement max 1000 token limit enforcement in api/src/services/utils/chunker.py
- [ ] T028 [US2] Add 100-token overlap functionality in api/src/services/utils/chunker.py
- [ ] T029 [US2] Validate chunking rules implementation in api/src/services/utils/chunker.py
- [ ] T030 [US2] Test chunking with various document structures

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - RAG Retrieval Service (Priority: P3)

**Goal**: A developer can build a service that retrieves relevant content from indexed documents based on user queries. The system should return the most relevant chunks with proper citations.

**Independent Test**: The RAG service can accept a query and return the top-5 most similar content chunks with source URLs for citations.

### Implementation for User Story 3

- [ ] T031 [P] [US3] Create RAG service in api/src/services/rag.py
- [ ] T032 [US3] Implement retrieve function with query embedding in api/src/services/rag.py
- [ ] T033 [US3] Add Qdrant search functionality in api/src/services/rag.py
- [ ] T034 [US3] Implement build_context function in api/src/services/rag.py
- [ ] T035 [US3] Handle source citations properly in api/src/services/rag.py
- [ ] T036 [US3] Test retrieval accuracy with sample queries

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Integration & Testing

**Purpose**: Integrate with existing chat route and comprehensive testing

- [ ] T037 [P] Update chat endpoint to use RAG service in api/src/routes/chat.py
- [ ] T038 [P] Modify streaming response to include real sources in api/src/routes/chat.py
- [ ] T039 Create unit tests for chunker utility in api/tests/test_chunker.py
- [ ] T040 Create unit tests for embeddings service in api/tests/test_embeddings.py
- [ ] T041 Create unit tests for RAG service in api/tests/test_rag.py
- [ ] T042 Create integration tests for indexing process in api/tests/test_indexing.py
- [ ] T043 Create end-to-end tests for chat integration in api/tests/test_chat_integration.py
- [ ] T044 Run indexing script and verify collection has ~50-60 points
- [ ] T045 Test retrieval with sample queries like "embodied intelligence"
- [ ] T046 Verify chat endpoint returns proper sources in streaming response

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T047 [P] Add logging configuration to all services
- [ ] T048 Add error handling for Qdrant unavailability
- [ ] T049 Update documentation in api/README.md
- [ ] T050 Run quickstart validation to ensure all works as expected
- [ ] T051 Verify all requirements from spec.md are met
- [ ] T052 Update quickstart guide with new functionality

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Integration & Testing (Phase 6)**: Depends on all desired user stories being complete
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
Task: "Create chunker utility in api/src/services/utils/chunker.py"
Task: "Create embeddings service in api/src/services/embeddings.py"
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