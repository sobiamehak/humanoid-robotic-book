# Quickstart Guide: AI-native textbook on Physical AI & Humanoid Robotics

**Feature Branch**: `1-ai-textbook` | **Date**: 2025-12-04
**Related Spec**: [specs/1-ai-textbook/spec.md](specs/1-ai-textbook/spec.md)
**Related Plan**: [specs/1-ai-textbook/plan.md](specs/1-ai-textbook/plan.md)

## Overview

This guide provides a quick overview of how to set up and run the AI-native Physical AI & Humanoid Robotics textbook locally. It includes instructions for both the Docusaurus frontend and the FastAPI backend, along with necessary external service configurations.

## Prerequisites

Before you begin, ensure you have the following installed:

-   **Node.js** (LTS version, e.g., 18.x or 20.x)
-   **Python 3.9+**
-   **Docker Desktop** (for running services like Qdrant locally, if not using cloud free tiers)
-   **Git**
-   **Poetry** (Python package manager, `pip install poetry`)
-   **Better Auth Account**: Create an account at [https://www.better-auth.com/](https://www.better-auth.com/) and obtain your API keys.
-   **Neon Serverless Postgres Account**: Set up a free tier instance at [https://neon.tech/](https://neon.tech/) and get your connection string.
-   **Qdrant Cloud Account**: Set up a free tier instance at [https://cloud.qdrant.io/](https://cloud.qdrant.io/) and get your API key and URL.
-   **OpenAI API Key**: Obtain your API key from OpenAI for ChatKit/Agents SDK.
-   **Claude API Key**: Obtain your API key from Anthropic for Claude 3.5/Opus.

## 1. Clone the Repository

```bash
git clone [REPOSITORY_URL]
cd humanoid-robotic-book
git checkout 1-ai-textbook
```

## 2. Backend Setup (FastAPI)

Navigate to the `backend/` directory.

```bash
cd backend
poetry install
```

Create a `.env` file in the `backend/` directory with the following variables:

```
DATABASE_URL="[YOUR_NEON_POSTGRES_CONNECTION_STRING]"
BETTER_AUTH_API_KEY="[YOUR_BETTER_AUTH_API_KEY]"
QDRANT_URL="[YOUR_QDRANT_CLOUD_URL]"
QDRANT_API_KEY="[YOUR_QDRANT_CLOUD_API_KEY]"
OPENAI_API_KEY="[YOUR_OPENAI_API_KEY]"
CLAUDE_API_KEY="[YOUR_CLAUDE_API_KEY]"
```

Run database migrations (if any) and start the FastAPI server:

```bash
poetry run uvicorn src.main:app --reload
```

The backend API will be accessible at `http://localhost:8000` (or configured port).

## 3. Frontend Setup (Docusaurus)

Navigate to the `frontend/` directory.

```bash
cd frontend
npm install
```

Create a `.env` file in the `frontend/` directory (or configure environment variables via Docusaurus config) with relevant backend API URL and other frontend-specific keys:

```
REACT_APP_API_URL="http://localhost:8000/v1"
REACT_APP_BETTER_AUTH_CLIENT_ID="[YOUR_BETTER_AUTH_CLIENT_ID]"
# Add other frontend specific env variables here
```

Start the Docusaurus development server:

```bash
npm start
```

The Docusaurus site will be accessible at `http://localhost:3000`.

## 4. Content Ingestion (RAG)

Before the RAG chatbot can function, the textbook content from the `docs/` directory needs to be processed and ingested into Qdrant. This will typically involve a separate script or a CI/CD pipeline step.

```bash
# Example command (replace with actual script once implemented):
poetry run python scripts/ingest_content.py --docs-path ../docs --qdrant-url $QDRANT_URL --qdrant-api-key $QDRANT_API_KEY
```

## 5. Running Tests

-   **Backend Tests**:
    ```bash
    cd backend
    poetry run pytest
    ```
-   **Frontend Tests**:
    ```bash
    cd frontend
    npm test
    ```

## 6. Deployment

-   **Frontend (GitHub Pages)**: Follow Docusaurus deployment guide for GitHub Pages.
-   **Backend (Vercel/Serverless)**: Follow FastAPI/Vercel deployment guide.

---

**Note**: This quickstart guide assumes basic familiarity with Node.js, Python, and the command line. For detailed instructions on Better Auth, Neon, Qdrant, OpenAI, or Claude API usage, please refer to their respective official documentation.
