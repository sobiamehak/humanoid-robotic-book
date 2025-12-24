# Implementation Plan: Book RAG Chatbot Backend

**Branch**: `1-book-rag-chatbot-backend` | **Date**: 2025-12-22 | **Spec**: [link](../spec.md)
**Input**: Feature specification from `/specs/1-book-rag-chatbot-backend/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a multi-agent RAG chatbot backend using the 'agents' library, Qdrant for retrieval, and OpenRouter for LLM. The system will accept user queries about a book on physical AI humanoid robotics, retrieve relevant information from Qdrant vector database, and generate contextual responses using OpenRouter API. The architecture includes Main, Retrieval, and Generation agents with handoff capabilities for complex queries.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: agents, qdrant-client, cohere, python-dotenv, asyncio, logging
**Storage**: Qdrant Cloud vector database (external service)
**Testing**: pytest for unit and integration tests
**Target Platform**: Linux/Mac/Windows server environment
**Project Type**: Backend service
**Performance Goals**: Handle up to 50 concurrent users, response time under 5 seconds average
**Constraints**: <5s p95 response time, handle off-topic queries gracefully, maintain 90% accuracy in retrieval
**Scale/Scope**: Single book content (12 chapters), multi-user support for hackathon demo

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Library-First: The RAG functionality should be modular and potentially reusable
- CLI Interface: The system should accept input via CLI and provide text output
- Test-First: All components must have tests before implementation
- Integration Testing: Focus on testing the agent coordination and external API integrations
- Observability: Proper logging and error handling for debugging

## Project Structure

### Documentation (this feature)

```text
specs/1-book-rag-chatbot-backend/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── rag_chatbot/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── main_agent.py
│   │   ├── retrieval_agent.py
│   │   └── generation_agent.py
│   ├── tools/
│   │   ├── __init__.py
│   │   └── retrieval_tool.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── query_models.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── qdrant_service.py
│   │   └── llm_service.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   └── main.py
├── .env.example
├── requirements.txt
└── README.md

tests/
├── unit/
│   ├── test_agents/
│   ├── test_tools/
│   └── test_services/
├── integration/
│   ├── test_agent_coordination.py
│   └── test_external_apis.py
└── contract/
    └── test_api_contracts.py
```

**Structure Decision**: Single backend project with modular components for agents, tools, and services. The structure separates concerns with dedicated modules for each agent type, external service integration, and configuration management.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |