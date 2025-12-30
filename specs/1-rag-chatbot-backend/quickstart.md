# Quickstart Guide: RAG Chatbot Backend

## Prerequisites
- Python 3.11
- uv package manager

## Setup

### 1. Clone and Navigate
```bash
cd api
```

### 2. Initialize Project
```bash
uv init
# Create .python-version with "3.11"
echo "3.11" > .python-version
```

### 3. Install Dependencies
```bash
uv add fastapi uvicorn fastembed agents qdrant-client pydantic pydantic-settings python-dotenv sse-starlette tiktoken httpx
uv add --dev pytest pytest-asyncio
uv sync
```

### 4. Configure Environment
```bash
# Copy .env.example to .env and fill in credentials
cp .env.example .env
# Add your GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY
```

### 5. Run Application
```bash
uv run uvicorn src.main:app --reload --port 8000
```

## Project Structure
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

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/api/health
```

### Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

## Testing
```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src
```

## Development
- The application runs with auto-reload enabled
- All configuration is loaded from environment variables
- Logging is configured for development debugging