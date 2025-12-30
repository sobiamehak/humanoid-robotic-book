# Data Model: RAG Chatbot Backend

## Entities

### ChatRequest
- **Purpose**: Represents a user's chat message request
- **Fields**:
  - `message`: str (required) - The user's chat message content
  - `selected_text`: str (optional) - Selected text context from the UI
  - `current_page`: str (optional) - Current page context for the chat

### ChatResponse
- **Purpose**: Represents the AI-generated response streamed to the client
- **Fields**:
  - `content`: str (optional) - The AI-generated response content
  - `sources`: list (optional) - List of source documents used in the response
  - `done`: bool (optional) - Indicates if the streaming is complete

### Configuration
- **Purpose**: Represents system configuration including external service credentials
- **Fields**:
  - `gemini_api_key`: str (required) - AI service authentication key
  - `qdrant_url`: str (required) - Vector database endpoint URL
  - `qdrant_api_key`: str (required) - Vector database authentication key

## Validation Rules

### ChatRequest Validation
- `message` must not be empty
- `selected_text` and `current_page` are optional fields
- All string fields must be valid UTF-8

### Configuration Validation
- All API keys must be non-empty strings
- Qdrant URL must be a valid URL format
- All fields are required for proper operation

## State Transitions

### Chat Request Processing
1. **Received**: ChatRequest received via POST /api/chat
2. **Processing**: Message is being processed by the AI service
3. **Streaming**: Response chunks are being sent via SSE
4. **Completed**: Final "done" event is sent

## Relationships

### ChatRequest → ChatResponse
- One ChatRequest generates one or more ChatResponse events during streaming
- The relationship is temporal, with multiple response chunks for one request