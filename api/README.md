# RAG Chatbot Backend API

This is a FastAPI-based backend for a Retrieval-Augmented Generation (RAG) chatbot that integrates with Qdrant for vector storage and Google's Gemini for AI processing.

## Features

- FastAPI-based REST API with async support
- Server-Sent Events (SSE) for streaming chat responses
- Qdrant integration for vector search
- Google Gemini integration for AI responses
- Environment-based configuration
- Health check endpoint
- CORS support for frontend integration

## Setup

1. Clone the repository
2. Navigate to the `api` directory
3. Install dependencies using uv:

```bash
cd api
uv sync
```

4. Create a `.env` file with your credentials:

```bash
cp .env.example .env
# Edit .env and add your credentials
```

## Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key
- `QDRANT_URL`: Your Qdrant cluster URL
- `QDRANT_API_KEY`: Your Qdrant API key

## Running the Application

```bash
cd api
uv run python -m src.main
```

Or using uvicorn directly:

```bash
uv run uvicorn src.main:app --reload --port 8000
```

## API Endpoints

### Health Check
- `GET /api/health` - Returns health status

### Chat
- `POST /api/chat` - Send a chat message and receive a streaming response

Example request:
```json
{
  "message": "Hello, how are you?",
  "selected_text": "Optional selected text context",
  "current_page": "Optional current page context"
}
```

## Project Structure

```
api/
├── src/
│   ├── main.py          # Main FastAPI application
│   ├── config/
│   │   └── settings.py  # Configuration and settings
│   ├── routes/
│   │   ├── health.py    # Health check endpoint
│   │   └── chat.py      # Chat endpoint
│   └── services/
│       ├── qdrant_service.py   # Qdrant integration
│       └── gemini_service.py   # Gemini integration
├── tests/
│   ├── test_health.py
│   ├── test_chat.py
│   └── test_integration.py
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

## Testing

Run the tests using pytest:

```bash
uv run pytest tests/
```

## Dependencies

- fastapi
- uvicorn
- qdrant-client
- google-generativeai
- pydantic
- pydantic-settings
- python-dotenv
- sse-starlette
- pytest
- httpx