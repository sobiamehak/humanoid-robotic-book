# Feature Specification: Book RAG Chatbot Backend

**Feature Branch**: `1-book-rag-chatbot-backend`
**Created**: 2025-12-22
**Status**: Draft
**Input**: User description: "Project Name: Book RAG Chatbot Backend
Overview:
Build a backend for a Retrieval-Augmented Generation (RAG) chatbot focused on a book about physical AI humanoid robotics. The book has 12 chapters and was generated using Claude with Docusaurus. The book's content is already vectorized and stored in a Qdrant vector database. The chatbot should use a multi-agent system to handle user queries, retrieving relevant information from Qdrant and generating responses using an LLM via OpenRouter API.
Key Requirements:

Data Storage: Use Qdrant Cloud for vector retrieval.
URL: https://3edd413a-51b8-47c1-b749-cae4cb09f488.europe-west3-0.gcp.cloud.qdrant.io:6333
API Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.Cva_t82sZPCvSeuoDkTWyLdsXK6gmBIu1S1kaKLil1g
Collection Name: book-rag-db
Chunk Size: 512
Chunk Overlap: 64
Top K: 5
Semantic Threshold: 0.0

Embeddings: Use Cohere API for embeddings if needed (API Key: G6fPCy4HS6YGybeO8HUseNEGIWR8vtlJgAg3BR3x). Assume data is already embedded in Qdrant.
LLM Integration: Use OpenRouter API for the language model.
API Key: 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
Model: Adapt from the example, but use OpenRouter's endpoint. Replace Gemini with a suitable model available on OpenRouter (e.g., anthropic/claude-3.5-sonnet or openai/gpt-4o).

Agent Architecture: Implement a multi-agent system similar to the provided example code using the 'agents' library (from agents import Agent, RunConfig, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled).
Main Agent: Handles initial query processing, detects if RAG retrieval is needed, and orchestrates responses.
Retrieval Agent: Queries Qdrant for relevant chunks based on user input.
Generation Agent: Uses retrieved context to generate a response via OpenRouter LLM.
Support handoffs between agents for complex queries.
Disable tracing as in the example.
Use AsyncOpenAI configured for OpenRouter's base URL.

Functionality:
Accept user queries about the book.
Retrieve top-k relevant chunks from Qdrant using semantic search.
Augment the prompt with retrieved context and send to LLM for response generation.
Handle edge cases like no relevant results or off-topic queries.
Run asynchronously for efficiency.

Dependencies:
Python libraries: agents, asyncio, dotenv, os, qdrant-client, cohere (if needed for re-embedding).
No additional installations beyond what's in the example.

Configuration:
Load keys from .env file as provided.
Adapt the example code's structure: Define models, agents, run config, and main async function.

Output:
The backend should be a runnable Python script that takes user input and outputs responses.
Ensure it's modular for easy extension.


Non-Functional Requirements:

Scalable and efficient for hackathon demo.
Error handling for API calls.
Logging for debugging.
Follow best practices for AI agent systems."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Query Book Content (Priority: P1)

A user interested in physical AI humanoid robotics submits a question about specific topics covered in the book. The system retrieves relevant information from the book's content and generates an accurate, contextual response based on the book's material.

**Why this priority**: This is the core functionality that delivers the primary value of the system - allowing users to interact with the book content through natural language queries.

**Independent Test**: The system can accept a user query about humanoid robotics concepts and return a response that contains information directly from the book's content, demonstrating successful RAG (Retrieval-Augmented Generation) functionality.

**Acceptance Scenarios**:

1. **Given** a user submits a question about humanoid robotics, **When** the system processes the query, **Then** it returns a response containing relevant information from the book's chapters
2. **Given** a user asks a specific question about content in Chapter 3, **When** the system performs semantic search in the vector database, **Then** it retrieves the most relevant chunks and generates an accurate response

---

### User Story 2 - Handle Off-Topic Queries (Priority: P2)

A user submits a query that is unrelated to the book's content about physical AI humanoid robotics. The system recognizes the query is off-topic and responds appropriately without fabricating information.

**Why this priority**: Essential for maintaining trust and preventing the system from providing inaccurate information about topics outside the book's scope.

**Independent Test**: The system can detect when a query is unrelated to the book content and respond with an appropriate message acknowledging the limitation rather than generating fabricated responses.

**Acceptance Scenarios**:

1. **Given** a user asks about topics unrelated to humanoid robotics, **When** the system evaluates the query relevance, **Then** it responds with an acknowledgment that the topic is outside the book's scope

---

### User Story 3 - Handle Complex Multi-Step Queries (Priority: P3)

A user submits a complex query that requires multiple steps of reasoning or information synthesis from different parts of the book. The system coordinates between multiple agents to process the query and generate a comprehensive response.

**Why this priority**: Enhances the system's ability to handle sophisticated queries that simple keyword matching cannot address.

**Independent Test**: The system can process complex queries requiring information from multiple chapters and synthesize that information into a coherent response.

**Acceptance Scenarios**:

1. **Given** a user asks a multi-faceted question requiring information from different chapters, **When** the multi-agent system coordinates retrieval and generation, **Then** it produces a comprehensive response synthesizing information from multiple sources

---

### Edge Cases

- What happens when the Qdrant vector database is temporarily unavailable?
- How does the system handle queries that return no relevant results from the semantic search?
- What occurs when the OpenRouter API is experiencing high latency or downtime?
- How does the system respond to extremely long or malformed user queries?
- What happens when multiple users submit queries simultaneously?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept user queries about the book content on physical AI humanoid robotics
- **FR-002**: System MUST retrieve top-5 relevant chunks from Qdrant using semantic search with configurable threshold
- **FR-003**: System MUST generate contextual responses using OpenRouter API with appropriate LLM model
- **FR-004**: System MUST implement a multi-agent architecture with Main, Retrieval, and Generation agents
- **FR-005**: System MUST support handoffs between agents for complex queries
- **FR-006**: System MUST handle edge cases like no relevant results or off-topic queries appropriately
- **FR-007**: System MUST run asynchronously to handle multiple concurrent requests efficiently
- **FR-008**: System MUST load configuration from environment variables for API keys and connection parameters
- **FR-009**: System MUST implement error handling for API calls to Qdrant and OpenRouter services
- **FR-010**: System MUST log operations for debugging and monitoring purposes

### Key Entities

- **User Query**: The input text from users seeking information about the book content
- **Retrieved Chunks**: Relevant text segments extracted from the vector database based on semantic similarity
- **Generated Response**: The final output produced by the LLM incorporating retrieved context
- **Agent System**: The multi-agent architecture coordinating query processing, retrieval, and response generation

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users receive relevant responses to book-related queries within 5 seconds on average
- **SC-002**: System achieves 90% accuracy in retrieving relevant book content for typical queries
- **SC-003**: At least 85% of user queries result in informative responses that directly reference book content
- **SC-004**: System handles up to 50 concurrent users without significant performance degradation during hackathon demo