# Quickstart Guide: RAG Chatbot Content Indexing

## Prerequisites
- Python 3.11
- uv package manager
- Access to Qdrant Cloud with API credentials
- Existing RAG Chatbot backend (from Part 1)

## Setup

### 1. Navigate to Project Directory
```bash
cd api
```

### 2. Ensure Dependencies are Installed
```bash
uv sync
```

### 3. Verify Environment Configuration
```bash
# Ensure .env file has QDRANT_URL and QDRANT_API_KEY set
cat .env
```

## Content Preparation

### 1. Prepare Content Files
```bash
# Ensure docs/ directory has the required files:
# - overview.md
# - chapter-01/*.md (lesson files)
# - chapter-02/*.md (lesson files)
# - chapter-03/*.md (lesson files)
ls docs/
```

## Indexing Process

### 1. Run the Indexing Script
```bash
uv run python scripts/index_content.py
```

### 2. Verify Indexing Success
```bash
# Check console output for summary of indexed chunks
# Should show ~50-60 chunks indexed
```

### 3. Verify in Qdrant Dashboard
```bash
# Log into Qdrant Cloud dashboard
# Confirm "textbook_content" collection exists with ~50-60 points
# Verify vectors are 384-dimensional with cosine distance
```

## Testing Retrieval

### 1. Test Retrieval Function
```bash
# Test in Python REPL
python -c "
from src.services.rag import retrieve
results = retrieve('embodied intelligence', top_k=5)
print(f'Retrieved {len(results)} chunks')
for i, result in enumerate(results):
    print(f'{i+1}. Score: {result[\"score\"]}, Text: {result[\"chunk\"][\"text\"][:100]}...')
"
```

### 2. Test Context Building
```bash
# Test context building with results
python -c "
from src.services.rag import retrieve, build_context
results = retrieve('machine learning', top_k=5)
context, sources = build_context(results)
print(f'Context length: {len(context)} characters')
print(f'Number of sources: {len(sources)}')
print('Sources:', sources)
"
```

## Integration Testing

### 1. Start the Backend Server
```bash
uv run uvicorn src.main:app --reload --port 8000
```

### 2. Test Chat Endpoint with RAG
```bash
# Send a query related to the indexed content
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is embodied intelligence?"}'
```

### 3. Verify Response Contains Sources
```bash
# Check that the response includes source citations
# The sources event should contain proper URLs for citations
```

## Project Structure
```
api/
├── src/
│   ├── services/
│   │   ├── __init__.py
│   │   ├── embeddings.py
│   │   ├── rag.py
│   │   ├── indexer.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── chunker.py
│   └── routes/
│       └── chat.py
├── scripts/
│   └── index_content.py
└── docs/
    ├── overview.md
    ├── chapter-01/
    │   └── *.md
    ├── chapter-02/
    │   └── *.md
    └── chapter-03/
        └── *.md
```

## Troubleshooting

### Common Issues
- **Qdrant Connection**: Verify QDRANT_URL and QDRANT_API_KEY in .env
- **Chunking Errors**: Ensure markdown files have proper ## headings
- **Embedding Issues**: Check that fastembed is properly installed
- **Indexing Failures**: Verify that the "textbook_content" collection can be created

### Verification Commands
```bash
# Check if dependencies are properly installed
uv run python -c "import fastembed; import qdrant_client; print('Dependencies OK')"

# Verify Qdrant connection
uv run python -c "
from qdrant_client import QdrantClient
from src.config.settings import settings
client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
collections = client.get_collections()
print('Collections:', [c.name for c in collections.collections])
"
```