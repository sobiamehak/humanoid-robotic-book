# Implementation Plan: RAG Chatbot Backend Setup and Core API Implementation

**Feature Branch**: `1-rag-chatbot-backend`
**Created**: 2025-12-27
**Status**: Draft
**Spec**: [specs/1-rag-chatbot-backend/spec.md](specs/1-rag-chatbot-backend/spec.md)

## Technical Context

### Architecture Overview
- **Framework**: FastAPI for high-performance async API
- **Package Manager**: uv for Python dependency management
- **Runtime**: Python 3.11
- **API Style**: REST API with Server-Sent Events (SSE) for streaming
- **Environment**: Configuration via environment variables
- **Structure**: src/, scripts/, tests/ directories

### Core Components
- **Health Endpoint**: Basic health check functionality
- **Chat Endpoint**: Streaming chat responses using SSE
- **Configuration**: Environment variable loading with Pydantic Settings
- **External Services**: Qdrant for vector storage, Gemini for AI processing

### Dependencies
- **Runtime**: fastapi, uvicorn, fastembed, agents, qdrant-client, pydantic, pydantic-settings, python-dotenv, sse-starlette, tiktoken, httpx
- **Dev**: pytest, pytest-asyncio

### Environment Variables
- GEMINI_API_KEY: AI service authentication
- QDRANT_URL: Vector database endpoint
- QDRANT_API_KEY: Vector database authentication

## Constitution Check

### Library-First Principle
- The backend will be structured as a cohesive library with clear separation of concerns
- Components will be independently testable and documented

### CLI Interface Principle
- The application will expose functionality via command-line startup
- Will support structured logging for observability

### Test-First Principle
- All components will have corresponding tests in the tests/ directory
- TDD approach will be followed with tests written before implementation

### Integration Testing Principle
- Integration tests will verify external service connections
- Contract tests will validate API endpoints

### Observability Principle
- Structured logging will be implemented for debugging and monitoring
- Health checks will provide system status visibility

## Phase 0: Research

### Research Tasks

1. **FastAPI SSE Implementation**
   - Decision: Use sse-starlette for Server-Sent Events
   - Rationale: Provides proper SSE support with FastAPI integration
   - Alternatives considered: Manual SSE implementation, other streaming libraries

2. **Qdrant Integration Patterns**
   - Decision: Use official qdrant-client library
   - Rationale: Official library provides proper async support and feature completeness
   - Alternatives considered: Direct HTTP API calls

3. **Configuration Management**
   - Decision: Use Pydantic Settings with python-dotenv
   - Rationale: Provides type validation and environment variable loading
   - Alternatives considered: Manual environment loading, other config libraries

4. **Dependency Management**
   - Decision: Use uv package manager with pyproject.toml
   - Rationale: Modern Python packaging with fast dependency resolution
   - Alternatives considered: pip + requirements.txt, poetry

## Phase 1: Design & Contracts

### Data Model

#### ChatRequest Entity
- **message**: str (required) - The user's chat message
- **selected_text**: str (optional) - Selected text context
- **current_page**: str (optional) - Current page context

#### ChatResponse Entity
- **content**: str - The AI-generated response
- **sources**: list - List of source documents used
- **done**: bool - Indicates if streaming is complete

#### Configuration Entity
- **gemini_api_key**: str - AI service authentication key
- **qdrant_url**: str - Vector database endpoint
- **qdrant_api_key**: str - Vector database authentication key

### API Contracts

#### Health Endpoint
```
GET /api/health
Response: 200 {"status": "healthy"}
```

#### Chat Endpoint
```
POST /api/chat
Content-Type: application/json
Request: {
  "message": "string",
  "selected_text": "string?",
  "current_page": "string?"
}
Response: 200 text/event-stream
Events:
- data: {"type": "chunk", "content": "string"}
- data: {"type": "sources", "sources": []}
- data: {"type": "done"}
```

### Project Structure
```
api/
├── .python-version
├── .env.example
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   └── routes/
│       ├── __init__.py
│       ├── health.py
│       └── chat.py
├── scripts/
│   └── __init__.py
└── tests/
    ├── __init__.py
    ├── test_health.py
    └── test_chat.py
```

### Quickstart Guide

1. **Setup Environment**
   ```bash
   cd api
   uv init
   # Create .python-version with "3.11"
   ```

2. **Install Dependencies**
   ```bash
   uv add fastapi uvicorn fastembed agents qdrant-client pydantic pydantic-settings python-dotenv sse-starlette tiktoken httpx
   uv add --dev pytest pytest-asyncio
   uv sync
   ```

3. **Configure Environment**
   ```bash
   # Copy .env.example to .env and fill in credentials
   cp .env.example .env
   # Add your GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY
   ```

4. **Run Application**
   ```bash
   uv run uvicorn src.main:app --reload --port 8000
   ```

5. **Test Endpoints**
   ```bash
   # Health check
   curl http://localhost:8000/api/health

   # Chat endpoint
   curl -X POST http://localhost:8000/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello"}'
   ```

## Phase 2: Implementation Tasks

### Task 1: Project Setup
- [ ] Initialize project with uv
- [ ] Create directory structure
- [ ] Add .python-version file
- [ ] Create __init__.py files

### Task 2: Dependency Management
- [ ] Add dependencies to pyproject.toml
- [ ] Run uv sync
- [ ] Verify all dependencies install correctly

### Task 3: Configuration
- [ ] Create .env.example
- [ ] Implement settings.py with Pydantic Settings
- [ ] Test environment variable loading

### Task 4: Health Endpoint
- [ ] Create health.py route
- [ ] Implement GET /api/health endpoint
- [ ] Add health check tests

### Task 5: Chat Endpoint
- [ ] Create chat.py route
- [ ] Define ChatRequest model
- [ ] Implement POST /api/chat endpoint with SSE
- [ ] Add streaming response functionality
- [ ] Add chat endpoint tests

### Task 6: Main Application
- [ ] Create main.py with FastAPI app
- [ ] Add CORS middleware
- [ ] Include health and chat routers
- [ ] Configure startup on port 8000

### Task 7: Testing
- [ ] Write unit tests for all components
- [ ] Write integration tests for API endpoints
- [ ] Verify all tests pass

## Success Criteria Verification

- [ ] Backend starts successfully without errors
- [ ] Health endpoint responds within 10 seconds
- [ ] Chat endpoint processes requests with 95% success rate
- [ ] All dependencies configured correctly with no import errors
- [ ] External service connections established
- [ ] Streaming responses work properly
- [ ] Concurrent request handling tested