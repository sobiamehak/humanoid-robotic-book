# Tasks: AI-native textbook on Physical AI & Humanoid Robotics

**Feature Branch**: `1-ai-textbook` | **Date**: 2025-12-04
**Related Spec**: [specs/1-ai-textbook/spec.md](specs/1-ai-textbook/spec.md)
**Related Plan**: [specs/1-ai-textbook/plan.md](specs/1-ai-textbook/plan.md)

## Summary

This document outlines the detailed, actionable tasks required to implement the AI-native textbook on Physical AI & Humanoid Robotics. Tasks are organized into phases, prioritizing foundational setup, core chapter content, and then specific bonus features, ensuring an incremental and testable delivery approach. Each task is granular and includes specific file paths for clarity, adhering to the specified checklist format.

## Implementation Strategy

The implementation will follow an MVP-first approach, iteratively delivering and validating each user story. Core infrastructure will be established first, followed by the content delivery system, and then the interactive and personalized features. Research will be concurrent with writing, and continuous integration will ensure code quality and reproducibility.

## Dependency Graph (User Story Completion Order)

User Story 1 (Read Textbook Chapters) -> User Story 3 (User Authentication & Profiling)
User Story 1 (Read Textbook Chapters) -> User Story 2 (Interact with RAG Chatbot)
User Story 3 (User Authentication & Profiling) -> User Story 4 (Personalize Chapter Content)
User Story 3 (User Authentication & Profiling) -> User Story 5 (Urdu Translation)

## Parallel Execution Examples

### User Story 1 (Read Textbook Chapters)
- T003: Install Docusaurus dependencies in frontend/
- T004: Create Docusaurus project structure in frontend/

### User Story 2 (Interact with RAG Chatbot)
- T017: Implement RAG chatbot query endpoint (FastAPI) in backend/src/api/chatbot.py
- T018: Develop frontend RAG chatbot UI component in frontend/src/components/Chatbot.tsx

### User Story 3 (User Authentication & Profiling)
- T024: Create User model for Neon Postgres in backend/src/models/user.py
- T025: Implement Better Auth signup/signin logic in backend/src/services/auth_service.py
- T026: Develop signup/signin UI pages in frontend/src/pages/Auth.tsx

### User Story 4 (Personalize Chapter Content)
- T031: Implement personalization logic in backend/src/services/personalization_service.py
- T032: Create "Personalize this chapter" button component in frontend/src/components/PersonalizeButton.tsx

### User Story 5 (Urdu Translation)
- T036: Implement Urdu translation logic (GPT-4o with caching) in backend/src/services/translation_service.py
- T037: Create "اردو میں ترجمہ کریں" button component in frontend/src/components/UrduTranslateButton.tsx

## Phase 1: Setup (Project Initialization)

- [x] T001 Create root project directories (backend/, frontend/, docs/) at project root
- [x] T002 Initialize Python backend project with Poetry in backend/
- [x] T004 Create Docusaurus project structure in frontend/
- [x] T003 Install Docusaurus dependencies in frontend/
- [x] T005 Configure Docusaurus base URL for GitHub Pages deployment in frontend/docusaurus.config.js
- [x] T006 Create initial `.env` files for backend and frontend for local development in backend/.env, frontend/.env

## Phase 2: Foundational (Blocking Prerequisites)

- [x] T007 Implement initial database schema for User and Chapter/Content Segment entities in backend/src/models/db_schema.py
- [x] T008 Configure database connection with Neon Serverless Postgres in backend/src/config.py
- [x] T009 Create script for ingesting textbook content into Qdrant in scripts/ingest_content.py
- [x] T010 Configure Qdrant client connection in backend/src/config.py
- [x] T011 Set up basic FastAPI application structure in backend/src/main.py

## Phase 3: User Story 1 - Read Textbook Chapters (Priority: P1)

**Story Goal**: Users can navigate through all textbook chapters and appendices, viewing theoretical concepts, code, simulations, and exercises.

**Independent Test**: Successfully deploy the Docusaurus site and verify that all 13 chapters and 2 appendices are accessible and display their intended content (theory, code, simulations, exercises).

- [X] T012 [US1] Create 13 empty chapter MDX files and 2 empty appendix MDX files in docs/
- [X] T013 [US1] Configure Docusaurus sidebar to reflect the 4 official modules and all chapters/appendices in frontend/sidebars.js
- [X] T014 [US1] Develop basic Docusaurus page template for chapters to include sections for theory, code, simulation, and exercises in frontend/src/components/ChapterLayout.tsx
- [X] T015 [US1] Implement placeholder content (e.g., "Coming Soon") for each section in docs/*.mdx

## Phase 4: User Story 3 - User Authentication & Profiling (Priority: P2)

**Story Goal**: New users can sign up and provide background info, existing users can sign in, and profiles are stored securely.

**Independent Test**: Successfully register a new user, log in, and verify user profile data (including background info) is correctly stored in Neon Postgres and retrievable.

- [X] T016 [P] [US3] Create User model (Pydantic/SQLAlchemy) in backend/src/models/user.py
- [X] T017 [P] [US3] Integrate Better Auth SDK into the backend in backend/src/services/auth_service.py
- [X] T018 [P] [US3] Create API endpoints for signup and signin using FastAPI in backend/src/api/auth.py
- [X] T019 [P] [US3] Develop frontend signup form to collect email, password, and background info in frontend/src/pages/Auth.tsx
- [X] T020 [P] [US3] Develop frontend signin form in frontend/src/pages/Auth.tsx
- [X] T021 [P] [US3] Implement user profile storage and retrieval using Neon Postgres in backend/src/services/user_profile_service.py
- [X] T022 [US3] Add basic profile display page in frontend/src/pages/Profile.tsx

## Phase 5: User Story 2 - Interact with RAG Chatbot (Priority: P1)

**Story Goal**: Users can query an embedded RAG chatbot for answers from the book or selected text, with citations.

**Independent Test**: Verify the RAG chatbot can answer 10 random questions from the book correctly, providing accurate citations, and can answer questions from selected text snippets.

- [X] T023 [P] [US2] Implement content chunking and vector embedding logic for ingestion into Qdrant in backend/src/services/content_ingestion.py
- [X] T024 [P] [US2] Create RAG retrieval logic using Qdrant and OpenAI/Claude embeddings in backend/src/services/rag_service.py
- [X] T025 [P] [US2] Develop FastAPI endpoint for RAG chatbot queries in backend/src/api/chatbot.py
- [X] T026 [P] [US2] Integrate OpenAI ChatKit/Agents SDK into the frontend in frontend/src/components/Chatbot.tsx
- [X] T027 [P] [US2] Develop RAG chatbot UI component in frontend/src/components/Chatbot.tsx
- [X] T028 [US2] Implement functionality for user to select text and query chatbot from selection in frontend/src/components/ChapterContent.tsx
- [X] T029 [US2] Display chatbot responses with exact section/page citations in frontend/src/components/Chatbot.tsx

## Phase 6: User Story 4 - Personalize Chapter Content (Priority: P2)

**Story Goal**: Chapter content adapts dynamically based on the logged-in user's background.

**Independent Test**: With different user profiles, verify that clicking "Personalize this chapter" on a sample chapter results in a noticeable and relevant content adaptation based on the profile.

- [X] T030 [P] [US4] Implement personalization logic using structured JSON prompts and function calling (GPT-4o/Claude) in backend/src/services/personalization_service.py
- [X] T031 [P] [US4] Create FastAPI endpoint to request personalized chapter content in backend/src/api/personalization.py
- [X] T032 [P] [US4] Develop "Personalize this chapter" button component in frontend/src/components/PersonalizeButton.tsx
- [X] T033 [US4] Integrate personalized content rendering into Docusaurus chapter pages in frontend/src/components/ChapterLayout.tsx
- [X] T034 [US4] Implement caching for personalized content in Neon Postgres/Qdrant in backend/src/services/caching_service.py

## Phase 7: User Story 5 - Urdu Translation (Priority: P2)

**Story Goal**: Real-time, high-quality Urdu translation of chapter content is available on demand.

**Independent Test**: Verify that clicking "اردو میں ترجمہ کریں" on any chapter provides a fluent and technically accurate Urdu translation of the content.

- [X] T035 [P] [US5] Implement Urdu translation logic using GPT-4o with caching in backend/src/services/translation_service.py
- [X] T036 [P] [US5] Create FastAPI endpoint to request Urdu translation of chapter content in backend/src/api/translation.py
- [X] T037 [P] [US5] Develop "اردو میں ترجمہ کریں" button component in frontend/src/components/UrduTranslateButton.tsx
- [X] T038 [US5] Integrate translated content rendering into Docusaurus chapter pages in frontend/src/components/ChapterLayout.tsx
- [X] T039 [US5] Implement caching for Urdu translations in Neon Postgres/Qdrant in backend/src/services/caching_service.py

## Phase 8: Polish & Cross-Cutting Concerns

- [X] T040 Ensure total running cost < $15/month (monitor free tier usage)
- [X] T041 Implement CI/CD for Docker container for all code in .github/workflows/ci.yaml
- [X] T042 Conduct thorough plagiarism checks on all content
- [X] T043 Record 5–8 min demo video showcasing key features
- [X] T044 Deploy frontend to GitHub Pages
- [X] T045 Deploy backend to Vercel/Serverless
- [X] T046 Update README.md with live URL, video link, and project overview
- [X] T047 Ensure Git history clearly shows Claude Code Subagent usage
