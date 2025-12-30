# Data Model: RAG Chatbot Content Indexing

## Entities

### DocumentChunk
- **Purpose**: Represents a processed segment of content with embedded vector representation
- **Fields**:
  - `id`: str (required) - Unique identifier for the chunk
  - `text`: str (required) - The actual text content of the chunk
  - `metadata`: dict (required) - Contains chapter, lesson, section title, source URL

### SourceMetadata
- **Purpose**: Contains information about the original document including file path and URLs for citations
- **Fields**:
  - `chapter`: str (required) - Chapter identifier
  - `lesson`: str (required) - Lesson identifier
  - `section_title`: str (required) - Title of the section
  - `source_url`: str (required) - URL for citation purposes
  - `file_path`: str (required) - Original file path

### EmbeddingVector
- **Purpose**: 384-dimensional vector representation of content for similarity search
- **Fields**:
  - `vector`: list[float] (required) - 384-dimensional embedding vector
  - `text_id`: str (required) - Reference to the original text chunk

### QueryResult
- **Purpose**: Contains retrieved chunks with similarity scores and source information
- **Fields**:
  - `chunk`: DocumentChunk (required) - The retrieved document chunk
  - `score`: float (required) - Similarity score
  - `vector`: EmbeddingVector (required) - The vector representation

## Validation Rules

### DocumentChunk Validation
- `id` must be a non-empty string
- `text` must be a non-empty string
- `metadata` must contain required fields (chapter, lesson, section_title, source_url)

### SourceMetadata Validation
- All fields must be non-empty strings
- `source_url` must be a valid URL format

### EmbeddingVector Validation
- `vector` must be a list of exactly 384 floats
- `text_id` must be a non-empty string

### QueryResult Validation
- `chunk` must be a valid DocumentChunk
- `score` must be a float between 0 and 1
- `vector` must be a valid EmbeddingVector

## State Transitions

### Chunk Processing
1. **Raw Content**: Markdown content loaded from file
2. **Chunked**: Content split into chunks with metadata
3. **Embedded**: Chunks with vector representations
4. **Indexed**: Chunks stored in vector database

### Query Processing
1. **Query Received**: User query string received
2. **Embedded**: Query converted to vector representation
3. **Searched**: Vector search performed in database
4. **Ranked**: Results ranked by similarity score
5. **Context Built**: Context string and sources prepared

## Relationships

### DocumentChunk → SourceMetadata
- One-to-one relationship: Each chunk has one metadata object

### DocumentChunk → EmbeddingVector
- One-to-one relationship: Each chunk has one vector representation

### QueryResult → DocumentChunk
- One-to-one relationship: Each query result contains one document chunk

### QueryResult → EmbeddingVector
- One-to-one relationship: Each query result contains one vector representation