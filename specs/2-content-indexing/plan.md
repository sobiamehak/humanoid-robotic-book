# Implementation Plan: RAG Chatbot Part 2: Content Indexing and RAG Service

**Feature Branch**: `2-content-indexing`
**Created**: 2025-12-27
**Status**: Draft
**Spec**: [specs/2-content-indexing/spec.md](specs/2-content-indexing/spec.md)

## Technical Context

### Architecture Overview
- **Framework**: Python services using existing FastAPI backend structure
- **Vector Database**: Qdrant Cloud with collection "textbook_content"
- **Embedding Model**: BAAI/bge-small-en-v1.5 (384-dimensional vectors)
- **File Processing**: Markdown chunking with token limits
- **Structure**: Services under src/services/, scripts under scripts/

### Core Components
- **Chunker Service**: Processes markdown files into chunks with metadata
- **Embeddings Service**: Generates vector embeddings using FastEmbed
- **Indexer Script**: Orchestrates the indexing process
- **RAG Service**: Handles retrieval and context building
- **Integration**: Connects with existing chat endpoint

### Dependencies
- **Runtime**: fastembed, qdrant-client, tiktoken, python-dotenv
- **Core**: pydantic, fastapi (from existing backend)

### Environment Variables
- QDRANT_URL, QDRANT_API_KEY (from existing backend)

## Constitution Check

### Library-First Principle
- Each service (chunker, embeddings, rag) will be self-contained and independently testable
- Services will have clear interfaces and documentation

### Test-First Principle
- Unit tests will be written for chunking logic, embedding generation, and retrieval functions
- Integration tests will verify the end-to-end indexing and retrieval process

### Integration Testing Principle
- Contract tests will validate the integration between RAG service and chat endpoint
- End-to-end tests will verify the complete flow from indexing to retrieval

### Observability Principle
- Structured logging will be implemented for indexing and retrieval operations
- Error handling will provide clear feedback for debugging

## Phase 0: Research

### Research Tasks

1. **FastEmbed Implementation**
   - Decision: Use fastembed with BAAI/bge-small-en-v1.5 model
   - Rationale: Lightweight, efficient, and produces 384-dimensional vectors as required
   - Alternatives considered: SentenceTransformers, custom embedding models

2. **Markdown Chunking Patterns**
   - Decision: Split by ## headings with token limit and overlap
   - Rationale: Maintains semantic coherence while respecting token constraints
   - Alternatives considered: Sentence-based splitting, fixed character limits

3. **Qdrant Integration Patterns**
   - Decision: Use qdrant-client for vector database operations
   - Rationale: Official client with proper async support and feature completeness
   - Alternatives considered: Direct HTTP API calls

4. **Token Counting Implementation**
   - Decision: Use tiktoken for accurate token counting
   - Rationale: Same tokenizer used by many LLMs, accurate for token limits
   - Alternatives considered: Character counting, word-based counting

## Phase 1: Design & Contracts

### Data Model

#### DocumentChunk Entity
- **id**: str - Unique identifier for the chunk
- **text**: str - The actual text content of the chunk
- **metadata**: dict - Contains chapter, lesson, section title, source URL

#### SourceMetadata Entity
- **chapter**: str - Chapter identifier
- **lesson**: str - Lesson identifier
- **section_title**: str - Title of the section
- **source_url**: str - URL for citation purposes
- **file_path**: str - Original file path

#### EmbeddingVector Entity
- **vector**: list[float] - 384-dimensional embedding vector
- **text_id**: str - Reference to the original text chunk

#### QueryResult Entity
- **chunk**: DocumentChunk - The retrieved document chunk
- **score**: float - Similarity score
- **vector**: EmbeddingVector - The vector representation

### API Contracts

#### RAG Service Interface
```
retrieve(query: str, top_k: int = 5) -> List[QueryResult]
Input: Query string and number of results to retrieve
Output: List of query results with chunks and scores

build_context(hits: List[QueryResult]) -> Tuple[str, List[dict]]
Input: List of query results
Output: Context string and list of sources for citations
```

### Project Structure
```
src/
├── services/
│   ├── __init__.py
│   ├── embeddings.py
│   ├── rag.py
│   ├── indexer.py
│   └── utils/
│       ├── __init__.py
│       └── chunker.py
scripts/
├── __init__.py
└── index_content.py
```

### Quickstart Guide

1. **Prepare Content Files**
   ```bash
   # Ensure docs/ directory has overview.md, chapter-01, chapter-02, chapter-03 lesson files
   ls docs/
   ```

2. **Run Indexing Script**
   ```bash
   uv run python scripts/index_content.py
   ```

3. **Verify Indexing**
   ```bash
   # Check Qdrant dashboard for ~50-60 points in textbook_content collection
   # Or query manually to verify content
   ```

4. **Test Retrieval**
   ```bash
   # Test retrieval in Python REPL
   python -c "from src.services.rag import retrieve; print(retrieve('embodied intelligence'))"
   ```

5. **Integration Test**
   ```bash
   # Start server and test chat endpoint
   uv run uvicorn src.main:app --reload --port 8000
   # POST to /api/chat with a query related to the indexed content
   ```

## Phase 2: Implementation Tasks

### Task 1: Create Service Files Structure
- [ ] Create directory structure for services
- [ ] Add __init__.py files to make directories Python packages

### Task 2: Implement Chunking Logic
- [ ] Create chunker.py with markdown processing functions
- [ ] Implement splitting by ## headings
- [ ] Add token counting with tiktoken
- [ ] Implement chunk size limits and overlap
- [ ] Extract and preserve metadata

### Task 3: Implement Embeddings Service
- [ ] Create embeddings.py with FastEmbed integration
- [ ] Implement embed_texts function
- [ ] Verify 384-dimensional vector output

### Task 4: Create Indexer Script
- [ ] Create index_content.py script
- [ ] Define Phase 1 file paths (overview.md, chapter-01, chapter-02, chapter-03 lessons)
- [ ] Integrate chunking and embedding services
- [ ] Connect to Qdrant Cloud using existing settings
- [ ] Create collection if not exists with proper schema
- [ ] Upsert chunks with metadata
- [ ] Add progress reporting

### Task 5: Implement RAG Service
- [ ] Create rag.py with retrieval functions
- [ ] Implement retrieve function with query embedding
- [ ] Implement build_context function
- [ ] Handle source citations properly

### Task 6: Integrate with Chat Route
- [ ] Update chat endpoint to use RAG service
- [ ] Modify streaming response to include real sources
- [ ] Test end-to-end functionality

### Task 7: Testing and Verification
- [ ] Write unit tests for all services
- [ ] Test indexing script with sample data
- [ ] Verify retrieval accuracy
- [ ] Run end-to-end integration test

## Success Criteria Verification

- [ ] Indexing process successfully stores between 50-60 chunks from specified documents
- [ ] Chunking algorithm respects the 1000 token maximum and 100 token overlap constraints
- [ ] RAG service retrieves the top-5 most relevant chunks for a given query
- [ ] Embedding generation uses BAAI/bge-small model producing 384-dimensional vectors
- [ ] Indexing script (index_content.py) completes execution without errors
- [ ] Retrieved results include proper source URLs for citation purposes
- [ ] Integration with chat endpoint works correctly and streams real sources