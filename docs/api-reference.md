# API Reference for Book RAG Chatbot Backend

## Overview

The Book RAG Chatbot Backend provides a multi-agent system for querying book content using Retrieval-Augmented Generation (RAG). The system consists of three main agents: Main, Retrieval, and Generation, which coordinate to process user queries.

## Architecture

### Agents

#### Main Agent
- Coordinates between Retrieval and Generation agents
- Handles query routing and overall flow control
- Detects complex and off-topic queries

#### Retrieval Agent
- Interfaces with the Qdrant vector database
- Performs semantic search on book content
- Supports diverse and focused search strategies for complex queries

#### Generation Agent
- Generates responses based on retrieved context
- Handles both simple and multi-step query responses
- Formats citations and references

### Services

#### Qdrant Service
- Manages vector database operations
- Handles search, insertion, and collection management
- Provides similarity search capabilities

#### LLM Service
- Interfaces with LLM providers (OpenRouter, etc.)
- Generates responses based on context
- Handles query relevance checking

#### Query Relevance Service
- Determines if queries are relevant to book content
- Provides relevance scoring
- Suggests related topics

## Configuration

### Environment Variables

- `QDRANT_URL`: URL for the Qdrant vector database
- `QDRANT_API_KEY`: API key for Qdrant (if required)
- `OPENROUTER_API_KEY`: API key for LLM provider
- `COHERE_API_KEY`: API key for Cohere (if used)
- `LOG_LEVEL`: Logging level (default: INFO)

## Usage

### CLI Interface

The system can be used via command line:

```bash
python -m src.rag_chatbot.main "Your query here"
```

### Programmatic Interface

```python
from src.rag_chatbot.main import rag_chatbot_system
from src.rag_chatbot.models.query_models import QueryRequest

query_request = QueryRequest(query="Your question about the book")
response = await rag_chatbot_system.process_query(query_request)
print(response.response)
```

## Error Handling

The system handles various error conditions:

- Off-topic queries are detected and responded to appropriately
- Network errors with external services are caught and logged
- Invalid queries are handled gracefully
- Database connection issues are managed with appropriate fallbacks

## Logging

The system provides comprehensive logging for monitoring and debugging:

- Query processing is logged with metadata
- Agent coordination is tracked
- Performance metrics are recorded
- Error conditions are logged with stack traces