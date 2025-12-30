---
description: "Task list for Text Selection Handler implementation"
---

# Tasks: Text Selection Handler and Additional Features

**Input**: Design documents from `/specs/001-text-selection-handler/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Basic tests included per specification requirements.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Project structure**: `docs/src/components/TextSelectionHandler/` as root for text selection handler components
- Adjust paths based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create directory structure for TextSelectionHandler component in docs/src/components/TextSelectionHandler/
- [ ] T002 [P] Create empty __init__.py files if needed for Python compatibility
- [ ] T003 Install required dependencies: google-generativeai
- [ ] T004 Set up TypeScript configuration for the component

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 [P] Create main TextSelectionHandler component in docs/src/components/TextSelectionHandler/index.tsx
- [ ] T006 [P] Create TextSelectionHandler CSS module in docs/src/components/TextSelectionHandler/styles.module.css
- [ ] T007 Create TypeScript types for selection events in docs/src/components/TextSelectionHandler/types.ts
- [ ] T008 Set up global event listeners for text selection detection
- [ ] T009 Verify component can be imported and used in Docusaurus layout

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Text Selection and Contextual Explanation (Priority: P1) 🎯 MVP

**Goal**: As a user reading the documentation, I want to select text and click an "Ask about this" button so that I can get contextual explanations about the selected content without having to manually copy and paste it into the chat. The system should detect my text selection and show a contextual button that, when clicked, opens the chat with the selected text automatically included in the query.

**Independent Test**: User can select text on any page, see the "Ask about this" button appear, click it, and have the chat open with the selected text automatically included in the query. The system responds with a contextual explanation of the selected text.

### Implementation for User Story 1

- [ ] T010 [P] [US1] Implement text selection detection with mouseup/touchend events in TextSelectionHandler
- [ ] T011 [US1] Implement "Ask about this" button positioning near selection in styles.module.css
- [ ] T012 [US1] Add minimum text selection length check (>10 characters)
- [ ] T013 [US1] Implement floating button display logic based on text selection
- [ ] T014 [US1] Integrate with existing ChatWidget to open and set input with selected text
- [ ] T015 [US1] Add button click functionality to send selected text as query
- [ ] T016 [US1] Implement button disappearance when selection is cleared
- [ ] T017 [US1] Test text selection functionality across different page types
- [ ] T018 [US1] Verify selected text is properly passed to chat backend
- [ ] T019 [US1] Add accessibility attributes to text selection button

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Navigation Links in Responses (Priority: P2)

**Goal**: As a user receiving responses from the chatbot, I want to see clickable navigation links to relevant documentation pages/sections so that I can easily navigate to related content and continue my learning journey. The system should include accurate links to relevant Docusaurus pages in its responses.

**Independent Test**: When the chatbot responds to a query, it includes clickable navigation links to relevant documentation sections that open in the appropriate location when clicked.

### Implementation for User Story 2

- [ ] T020 [P] [US2] Update ChatMessage component to parse navigation links in responses
- [ ] T021 [US2] Implement clickable navigation link rendering in responses
- [ ] T022 [US2] Create navigation link format detection and parsing logic
- [ ] T023 [US2] Add proper styling for navigation links in chat messages
- [ ] T024 [US2] Implement URL validation for navigation links
- [ ] T025 [US2] Add navigation link click handling with proper routing
- [ ] T026 [US2] Test navigation link functionality with various response formats
- [ ] T027 [US2] Verify navigation links open in correct location
- [ ] T028 [US2] Add error handling for invalid navigation links

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Learning Guidance and Recommendations (Priority: P2)

**Goal**: As a user interacting with the chatbot, I want to receive meaningful learning guidance such as next steps, overviews, prerequisites, and recommendations so that I can better navigate my learning path through the textbook. The system should provide helpful guidance based on the context of my questions and current position in the material.

**Independent Test**: When users ask questions or engage with specific topics, the system provides relevant learning guidance including next steps, overviews, prerequisites, or recommendations for further study.

### Implementation for User Story 3

- [ ] T029 [P] [US3] Update system prompt template to include learning guidance instructions
- [ ] T030 [US3] Implement learning guidance detection and parsing in responses
- [ ] T031 [US3] Create learning guidance display component for chat messages
- [ ] T032 [US3] Add proper styling for learning guidance content
- [ ] T033 [US3] Implement guidance type classification (next step, prerequisite, etc.)
- [ ] T034 [US3] Add guidance content formatting and display
- [ ] T035 [US3] Test learning guidance with various query types
- [ ] T036 [US3] Verify guidance content is relevant and helpful
- [ ] T037 [US3] Add error handling for malformed guidance content

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Gemini Integration with Google Generative Language SDK (Priority: P1)

**Goal**: As a system, I need to use the Google Generative Language SDK to call Gemini with full streaming support so that users receive responses in real-time with proper streaming capabilities. The system should integrate with Gemini models via the Google Generative Language SDK for optimal performance and streaming.

**Independent Test**: The system successfully connects to Gemini via Google Generative Language SDK and streams responses token by token to the frontend for real-time display.

### Implementation for User Story 4

- [ ] T038 [P] [US4] Create LLM service in src/services/llm.py using Google Generative Language SDK
- [ ] T039 [US4] Implement Gemini model configuration (gemini-1.5-flash/gemini-1.5-pro)
- [ ] T040 [US4] Set up streaming response functionality with proper event handling
- [ ] T041 [US4] Update system prompt with text selection and page context handling
- [ ] T042 [US4] Implement proper error handling for Gemini API calls
- [ ] T043 [US4] Add API key configuration and validation
- [ ] T044 [US4] Test streaming responses with various query types
- [ ] T045 [US4] Verify response streaming works with existing SSE infrastructure
- [ ] T046 [US4] Add performance monitoring for response times

**Checkpoint**: At this point, all user stories should work independently

---

## Phase 7: Integration & Testing

**Purpose**: End-to-end integration and comprehensive testing

- [ ] T047 [P] Update /api/chat endpoint to handle selected_text and current_page parameters
- [ ] T048 [P] Integrate text selection context into chat request processing
- [ ] T049 Update ChatWidget to capture and send current page context
- [ ] T050 Add navigation link generation to response processing
- [ ] T051 Add learning guidance generation to response processing
- [ ] T052 Test complete user flow from text selection to response
- [ ] T053 Verify all functional requirements from spec are met
- [ ] T054 Test cross-browser compatibility (Chrome, Firefox, Safari, Edge)
- [ ] T055 Verify performance goals (response time <3s, 10+ concurrent users)
- [ ] T056 Test responsive design on mobile devices

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T057 [P] Add comprehensive error handling throughout components
- [ ] T058 Add accessibility improvements (keyboard navigation, screen reader support)
- [ ] T059 Update documentation in quickstart guide with implementation details
- [ ] T060 Run final validation to ensure all requirements are met
- [ ] T061 Verify success criteria from spec are achieved
- [ ] T062 Update quickstart guide with new functionality

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Integration & Testing (Phase 7)**: Depends on all desired user stories being complete
- **Polish (Phase 8)**: Depends on all previous phases

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Builds on US1-2 but should be independently testable
- **User Story 4 (P1)**: Can start after Foundational (Phase 2) - Builds on US1-3 but should be independently testable

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority
- Each story should be independently testable

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Components within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

### Parallel Example: User Story 1

```bash
# Launch all parallel tasks for User Story 1 together:
Task: "Implement text selection detection with mouseup/touchend events in TextSelectionHandler"
Task: "Implement \"Ask about this\" button positioning near selection in styles.module.css"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 4 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 - Text Selection and Contextual Explanation
4. Complete Phase 6: User Story 4 - Gemini Integration
5. **STOP and VALIDATE**: Test User Stories 1 & 4 together for basic functionality
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Stories 1 & 4 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Stories 1 & 4 (P1 stories)
   - Developer B: User Story 2 (P2 story)
   - Developer C: User Story 3 (P2 story)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [US1/US2/US3/US4] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests pass after implementation
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence