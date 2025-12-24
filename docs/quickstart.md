# Quickstart Guide for Book RAG Chatbot Backend

This guide will help you get the Book RAG Chatbot Backend up and running quickly.

## Prerequisites

- Python 3.11+
- pip package manager
- Access to Qdrant vector database (cloud or local)
- API key for your chosen LLM provider (OpenRouter, OpenAI, etc.)

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <repo-directory>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys and configuration
   ```

## Configuration

Edit the `.env` file with your specific configuration:

```env
# Qdrant Configuration
QDRANT_URL=your-qdrant-url
QDRANT_API_KEY=your-qdrant-api-key

# LLM Provider Configuration
OPENROUTER_API_KEY=your-openrouter-api-key

# Logging Configuration
LOG_LEVEL=INFO
```

## Running the Application

### CLI Mode

To run a single query from the command line:

```bash
python -m src.rag_chatbot.main "What is bipedal locomotion?"
```

### As a Library

To use the system programmatically:

```python
import asyncio
from src.rag_chatbot.main import rag_chatbot_system
from src.rag_chatbot.models.query_models import QueryRequest

async def main():
    query_request = QueryRequest(query="What is bipedal locomotion?")
    response = await rag_chatbot_system.process_query(query_request)
    print(response.response)

asyncio.run(main())
```

## Health Check

To check the health of the system:

```python
from src.rag_chatbot.health_check import health_checker

health_status = asyncio.run(health_checker.check_system_health())
print(health_status)
```

## Key Features

1. **Multi-Agent Architecture**: Main, Retrieval, and Generation agents work together
2. **Off-Topic Query Detection**: Automatically identifies and responds to queries outside the book scope
3. **Complex Query Processing**: Handles multi-step queries requiring information from multiple chapters
4. **Citation Support**: Provides references to source material
5. **Comprehensive Logging**: Full visibility into system operations

## Troubleshooting

- If you get API errors, verify your API keys in the `.env` file
- Check that your Qdrant instance is running and accessible
- Enable DEBUG logging to see more detailed information