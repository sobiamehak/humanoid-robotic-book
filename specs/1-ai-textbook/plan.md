# Implementation Plan: AI-native textbook on Physical AI & Humanoid Robotics

**Branch**: `1-ai-textbook` | **Date**: 2025-12-04 | **Spec**: [specs/1-ai-textbook/spec.md](specs/1-ai-textbook/spec.md)
**Input**: Feature specification from `/specs/1-ai-textbook/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The plan is to create an interactive, AI-native textbook on Physical AI & Humanoid Robotics using a Docusaurus frontend deployed on GitHub Pages and a FastAPI backend (Vercel/Serverless). Data management will utilize Neon Serverless Postgres for user profiles and cached translations, and Qdrant Cloud (Free Tier) for the vector store of book chunks. User authentication will be handled by Better Auth, and core interactive features like the embedded RAG chatbot (with selected-text mode), personalization, and Urdu translation will leverage OpenAI ChatKit/Agents SDK, Claude 3.5/Opus, and cached GPT-4o. The project will follow a phased development approach covering foundation setup, core chapter content creation, bonus feature implementation, and final polish/demo preparation, adhering to a research-concurrent strategy.

## Technical Context

**Language/Version**: Python 3.9+ (for FastAPI backend), JavaScript/TypeScript (for Docusaurus frontend)
**Primary Dependencies**: Docusaurus, FastAPI, Neon Serverless Postgres, Qdrant Cloud, Better Auth, OpenAI Agents SDK / ChatKit, Claude 3.5/Opus, GPT-4o
**Storage**: Neon Serverless Postgres (user profiles, cached translations), Qdrant Cloud (vector store for book chunks + personalized versions)
**Testing**: Functional testing of all features, quality validation checks as defined in the success criteria (RAG chatbot accuracy, Urdu translation accuracy, personalization impact), CI checks for code in Docker container.
**Target Platform**: Web (GitHub Pages for frontend, Vercel/Serverless for backend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: Real-time (sub-second) translation and personalization, efficient RAG chatbot responses (under 2 seconds for typical queries).
**Constraints**: Total running cost < $15/month (free tiers only), all content in `/docs` as Markdown/MDX.
**Scale/Scope**: 13 chapters + 2 appendices, comprehensive bonus features (RAG chatbot, authentication, personalization, Urdu translation), target audience of undergraduate/graduate students and professionals.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Accuracy via up-to-date research**: The plan incorporates a research-concurrent approach and specifies primary/secondary sources (ICRA/IROS/RSS 2023–2025 papers, arXiv 2024–2025, NVIDIA Isaac, ROS 2 docs) for content creation and verification. **[PASS]**
- **II. Clarity for advanced students**: The plan outlines the creation of 13 chapters + 2 appendices, each with theory, Python/ROS 2 code, simulations, and exercises, tailored for the specified target audience. **[PASS]**
- **III. Interactivity first**: The plan explicitly includes the implementation of a RAG chatbot, personalization features, and Urdu translation, all designed to enhance user interactivity. **[PASS]**
- **IV. Personalization and inclusivity**: The plan directly addresses personalization based on user background and high-quality, real-time Urdu translation, aligning with inclusivity principles. **[PASS]**
- **V. Reproducibility of all experiments**: The plan mandates that all code will run in a Docker container with CI checks, ensuring reproducibility of experiments. **[PASS]**

## Project Structure

### Documentation (this feature)

```text
specs/1-ai-textbook/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/           # For Neon Postgres schemas (user profiles, cached translations)
│   ├── services/         # For RAG logic, translation, personalization, Better Auth integration
│   └── api/              # FastAPI endpoints
└── tests/

frontend/
├── src/
│   ├── components/       # Docusaurus components (buttons, custom UI)
│   ├── pages/            # Docusaurus pages (e.g., login, profile)
│   └── services/         # Frontend services (API calls, RAG chatbot integration)
└── tests/

docs/                     # All textbook content (Markdown/MDX chapters and appendices)
```

**Structure Decision**: Selected a web application structure with separate `backend/`, `frontend/`, and `docs/` directories to clearly delineate responsibilities and leverage Docusaurus for content management.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
