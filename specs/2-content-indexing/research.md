# Research: RAG Chatbot Content Indexing Implementation

## FastEmbed Implementation

### Decision: Use fastembed with BAAI/bge-small-en-v1.5 model
- **Rationale**: Lightweight, efficient, and produces 384-dimensional vectors as required
- **Alternatives considered**:
  - SentenceTransformers: More complex setup, larger models
  - Custom embedding models: Requires training and maintenance

## Markdown Chunking Patterns

### Decision: Split by ## headings with token limit and overlap
- **Rationale**: Maintains semantic coherence while respecting token constraints
- **Alternatives considered**:
  - Sentence-based splitting: May break semantic context
  - Fixed character limits: Doesn't respect document structure

## Qdrant Integration Patterns

### Decision: Use qdrant-client for vector database operations
- **Rationale**: Official client with proper async support and feature completeness
- **Alternatives considered**:
  - Direct HTTP API calls: More complex implementation, no built-in error handling

## Token Counting Implementation

### Decision: Use tiktoken for accurate token counting
- **Rationale**: Same tokenizer used by many LLMs, accurate for token limits
- **Alternatives considered**:
  - Character counting: Inaccurate for token-based models
  - Word-based counting: Doesn't reflect actual tokenization

## Vector Dimension Verification

### Decision: Confirm 384-dimensional vectors from BAAI/bge-small model
- **Rationale**: Matches requirement for Qdrant collection configuration
- **Verification**: BAAI/bge-small produces 384-dimensional embeddings

## Content File Structure

### Decision: Process markdown files following the expected structure
- **Rationale**: Organized content hierarchy allows for proper metadata extraction
- **Structure**: overview.md, chapter-01/lessons, chapter-02/lessons, chapter-03/lessons

## Metadata Extraction Strategy

### Decision: Extract chapter, lesson, section title, and generate source URLs
- **Rationale**: Enables proper citations and source tracking
- **Implementation**: Parse file paths and document structure to extract meaningful metadata