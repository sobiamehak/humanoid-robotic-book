---
id: 2
title: content-indexing-plan
stage: plan
date: 2025-12-27
surface: agent
model: Claude Sonnet 4.5
feature: content-indexing
branch: 2-content-indexing
user: mehak
command: /sp.plan
labels: ["planning", "architecture", "content-indexing", "rag", "qdrant", "vector-database"]
links:
  spec: "specs/2-content-indexing/spec.md"
  plan: "specs/2-content-indexing/plan.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/2-content-indexing/plan.md"
  - "specs/2-content-indexing/research.md"
  - "specs/2-content-indexing/data-model.md"
  - "specs/2-content-indexing/quickstart.md"
tests: []
outcome: "Implementation plan created for RAG Chatbot content indexing with all required components"
evaluation: "Plan covers architecture, dependencies, chunking logic, embeddings, and integration with existing backend"
---

# Prompt

```
RAG Chatbot Part 2: Content Indexing and RAG Service
Concise Implementation Plan

Create Service Files
Add to src/services/:
embeddings.py, rag.py, indexer.py, utils/chunker.py
Add scripts/index_content.py

Chunking Logic (src/services/utils/chunker.py)
Load markdown files from ../docs/docs/
Split by ##  headings → each section = one chunk
If chunk >1000 tokens (use tiktoken), split further with 100-token overlap
Extract metadata: chapter, lesson, section title, source URL (e.g., /chapter-01-foundations/lesson-01-intro)
Return list of dicts: id, text, metadata

Embeddings Service (src/services/embeddings.py)
Use FastEmbed with model BAAI/bge-small-en-v1.5
Single function embed_texts(texts: list[str]) → list[list[float]]
Confirm 384-dim vectors

Indexer Script (scripts/index_content.py)
Define Phase 1 file paths: overview.md + all lesson md files in chapters 01-03
Chunk all files using chunker
Generate embeddings
Connect to Qdrant Cloud (use settings.QDRANT_URL/API_KEY)
Create collection textbook_content (vector size 384, cosine distance) if not exists
Upsert ~50-60 points with payload metadata
Print summary: total chunks indexed
Run once: uv run python scripts/index_content.py

RAG Service (src/services/rag.py)
retrieve(query: str, top_k: int = 5) function:
Embed query
Search Qdrant collection → return hits
Extract chunks + metadata

build_context(hits) function:
Concatenate chunk texts (ordered by score)
Collect sources list: {title, url} for citations
Return context_str, sources_list


Integrate into Chat Route (src/routes/chat.py)
Import rag service
In /api/chat handler:
Call retrieve(message)
Call build_context()
For now, stream placeholder response + real sources event
Stream: chunk events (e.g., "Context retrieved..."), sources event (real list), done


Verification
Run indexer → confirm collection in Qdrant dashboard has ~50-60 points
Test query manually in Python REPL: retrieve top-5 for "embodied intelligence" → relevant chunks
Start server → POST chat request → verify sources event contain
```

# Response

I have successfully created the implementation plan for the RAG Chatbot Part 2: Content Indexing and RAG Service. The following artifacts have been created:

1. **Implementation Plan**: `specs/2-content-indexing/plan.md`
   - Technical context with architecture overview
   - Constitution compliance check
   - Detailed research findings with technology decisions
   - Data models for all entities
   - API contracts and interface definitions
   - Complete project structure and quickstart instructions
   - Implementation tasks broken down by phases

2. **Research Document**: `specs/2-content-indexing/research.md`
   - Technology decisions and rationale
   - Alternatives considered for each major component

3. **Data Model**: `specs/2-content-indexing/data-model.md`
   - Entity definitions for DocumentChunk, SourceMetadata, EmbeddingVector, and QueryResult
   - Validation rules and relationships

4. **Quickstart Guide**: `specs/2-content-indexing/quickstart.md`
   - Setup and indexing instructions
   - Testing and verification procedures
   - Troubleshooting guide

5. **PHR Record**: `history/prompts/content-indexing/2-content-indexing-plan.plan.prompt.md`

The plan covers all required components including:
- Chunking logic with heading-based splitting and token limits
- Embeddings service using FastEmbed with BAAI/bge-small model
- Indexer script for populating Qdrant collection
- RAG service for retrieval and context building
- Integration with existing chat endpoint
- Verification procedures for all components

All specifications align with the feature requirements from the original specification and are ready for the next phase of implementation.