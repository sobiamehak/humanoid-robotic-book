# Feature Specification: RAG Chatbot Part 2: Content Indexing and RAG Service

**Feature Branch**: `2-content-indexing`
**Created**: 2025-12-27
**Status**: Draft
**Input**: User description: "RAG Chatbot Part 2: Content Indexing and RAG Service
Target audience: Developers implementing data handling for the RAG chatbot
Focus: Indexing textbook content into Qdrant and building RAG query/retrieve/rank services
Success criteria:

Indexes ~50-60 chunks from specified docs/ files with metadata preserved
Implements chunking rules: split by ## headings, max 1000 tokens, 100 token overlap
RAG service generates embeddings with Qdrant FastEmbed and retrieves top-5 similar chunks
Builds context for LLM with source URLs for citations
Script index_content.py runs successfully without errors

Constraints:

Use Qdrant Cloud free tier for vector store, collection: textbook_content
Embeddings: BAAI/bge-small model, 384-dimensional vectors
Content: Limit to Phase 1 files (overview.md, chapter-01, chapter-02, chapter-03 lessons)
Format: Python scripts and services under src/services/ and scripts/

Not building:

LLM response generation (integrated in backend core)
Frontend UI for displaying indexed content
Additional"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Content Indexing (Priority: P1)

A developer needs to index textbook content into a vector database so that the RAG chatbot can retrieve relevant information. The system should process markdown files and store them with proper metadata for later retrieval.

**Why this priority**: This is foundational for the RAG functionality. Without indexed content, the chatbot cannot provide accurate responses based on the textbook material.

**Independent Test**: The indexing script processes markdown files and stores them in Qdrant with preserved metadata. The system can verify that content has been properly indexed.

**Acceptance Scenarios**:

1. **Given** markdown files exist in docs/ directory, **When** the index_content.py script runs, **Then** content is stored in Qdrant collection with preserved metadata
2. **Given** content exists in Qdrant, **When** a query is made, **Then** the system can retrieve the indexed content

---

### User Story 2 - Content Chunking (Priority: P2)

A developer needs to split large documents into smaller chunks that maintain context while being suitable for embedding and retrieval. The system should follow specific chunking rules to optimize for search quality.

**Why this priority**: Proper chunking is essential for retrieval quality. Poorly chunked content will result in irrelevant or incomplete responses from the chatbot.

**Independent Test**: The system can take a large markdown document and split it according to the specified rules: by ## headings, max 1000 tokens, with 100-token overlap.

**Acceptance Scenarios**:

1. **Given** a large markdown document, **When** chunking rules are applied, **Then** the document is split into chunks of maximum 1000 tokens each
2. **Given** a document with ## headings, **When** chunking occurs, **Then** splits happen at heading boundaries where possible
3. **Given** chunked content, **When** overlap is applied, **Then** adjacent chunks have 100-token overlap for context preservation

---

### User Story 3 - RAG Retrieval Service (Priority: P3)

A developer needs to build a service that can retrieve relevant content from the indexed documents based on user queries. The system should return the most relevant chunks with proper citations.

**Why this priority**: This enables the core RAG functionality that allows the chatbot to ground its responses in the indexed content with proper citations.

**Independent Test**: The RAG service can accept a query and return the top-5 most similar content chunks with source URLs for citations.

**Acceptance Scenarios**:

1. **Given** a user query, **When** the RAG service searches indexed content, **Then** it returns the top-5 most relevant chunks
2. **Given** retrieved chunks, **When** the service formats the response, **Then** source URLs are included for citations

---

### Edge Cases

- What happens when the Qdrant service is unavailable during indexing?
- How does the system handle documents that exceed maximum token limits?
- What occurs when the embedding model fails to process content?
- How does the system handle documents with no ## headings for chunking?
- What happens when there are no relevant results for a query?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST index ~50-60 chunks from specified docs/ files with metadata preserved
- **FR-002**: System MUST implement chunking rules: split by ## headings, max 1000 tokens, 100 token overlap
- **FR-003**: System MUST generate embeddings using Qdrant FastEmbed with BAAI/bge-small model
- **FR-004**: System MUST store content in Qdrant collection named "textbook_content"
- **FR-005**: System MUST retrieve top-5 similar chunks based on semantic similarity
- **FR-006**: System MUST build context for LLM with source URLs for citations
- **FR-007**: System MUST process markdown files: overview.md, chapter-01, chapter-02, chapter-03 lessons
- **FR-008**: System MUST use 384-dimensional vectors for embeddings
- **FR-009**: Script index_content.py MUST run successfully without errors
- **FR-010**: System MUST preserve document metadata during indexing

### Key Entities *(include if feature involves data)*

- **DocumentChunk**: Represents a processed segment of content with embedded vector representation
- **SourceMetadata**: Contains information about the original document including file path and URLs for citations
- **EmbeddingVector**: 384-dimensional vector representation of content for similarity search
- **QueryResult**: Contains retrieved chunks with similarity scores and source information

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Indexing process successfully stores between 50-60 chunks from the specified documents
- **SC-002**: Chunking algorithm respects the 1000 token maximum and 100 token overlap constraints
- **SC-003**: RAG service retrieves the top-5 most relevant chunks for a given query with 90%+ accuracy
- **SC-004**: Embedding generation uses BAAI/bge-small model producing 384-dimensional vectors
- **SC-005**: Indexing script (index_content.py) completes execution without errors
- **SC-006**: Retrieved results include proper source URLs for citation purposes