# Data Model: Book RAG Chatbot Backend

## Entities

### User Query
**Description**: The input text from users seeking information about the book content
**Fields**:
- query_text (string): The actual question or text from the user
- query_id (string): Unique identifier for the query
- timestamp (datetime): When the query was submitted
- user_context (dict): Optional additional context about the user session

### Retrieved Chunks
**Description**: Relevant text segments extracted from the vector database based on semantic similarity
**Fields**:
- chunk_id (string): Unique identifier for the text chunk
- content (string): The actual text content of the chunk
- score (float): Similarity score from the semantic search
- source_document (string): Reference to the original document/chapter
- metadata (dict): Additional information about the chunk location

### Generated Response
**Description**: The final output produced by the LLM incorporating retrieved context
**Fields**:
- response_id (string): Unique identifier for the response
- content (string): The generated response text
- query_id (string): Reference to the original query
- source_chunks (list): List of chunk IDs used to generate the response
- timestamp (datetime): When the response was generated
- confidence_score (float): Estimated confidence in the response quality

### Agent State
**Description**: State information for the multi-agent system
**Fields**:
- agent_id (string): Unique identifier for the agent
- current_task (string): What the agent is currently doing
- context (dict): Information being passed between agents
- status (string): Current status (idle, processing, waiting)

## Relationships

- User Query → Generated Response (one-to-one)
- User Query → Retrieved Chunks (one-to-many)
- Retrieved Chunks → Generated Response (many-to-one)
- Agent State → User Query (many-to-one, for tracking agent work)

## Validation Rules

- User Query must have non-empty query_text
- Retrieved Chunks must have content and score fields
- Generated Response must be based on at least one retrieved chunk
- Query and response timestamps must be valid

## State Transitions

### User Query State
- `received` → `processing` → `completed` | `error`

### Agent State
- `idle` → `assigned` → `processing` → `completed` | `failed`