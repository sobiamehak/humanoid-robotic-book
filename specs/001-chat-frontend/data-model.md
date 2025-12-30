# Data Model: RAG Chatbot Frontend Integration

## Entities

### ChatMessage
- **Purpose**: Represents a single message in the chat conversation
- **Fields**:
  - `id`: string (required) - Unique identifier for the message
  - `content`: string (required) - The text content of the message
  - `sender`: 'user' | 'bot' (required) - Indicates whether the message is from user or bot
  - `timestamp`: Date (required) - When the message was created/sent
  - `status`: 'sending' | 'sent' | 'delivered' | 'error' (optional) - Message delivery status
  - `sources`: SourceCitation[] (optional) - Source citations if this is a bot response

### SourceCitation
- **Purpose**: Contains information about sources referenced in a bot response
- **Fields**:
  - `title`: string (required) - Title of the source document
  - `url`: string (required) - URL to the source document
  - `relevance`: number (optional) - Relevance score (0-1)
  - `expanded`: boolean (optional) - Whether the citation is expanded in UI

### ChatSession
- **Purpose**: Represents the current chat session state
- **Fields**:
  - `id`: string (required) - Unique identifier for the session
  - `messages`: ChatMessage[] (required) - List of messages in the session
  - `isOpen`: boolean (required) - Whether the chat panel is open
  - `isLoading`: boolean (required) - Whether a response is currently being loaded
  - `error`: string | null (optional) - Any error message for the session

### SSEData
- **Purpose**: Represents data received via Server-Sent Events
- **Fields**:
  - `event`: 'chunk' | 'sources' | 'done' (required) - Type of event received
  - `data`: string (required) - The actual data payload

## Validation Rules

### ChatMessage Validation
- `id` must be a non-empty string
- `content` must be a non-empty string
- `sender` must be either 'user' or 'bot'
- `timestamp` must be a valid Date object
- If `sender` is 'bot', `sources` may be present

### SourceCitation Validation
- `title` must be a non-empty string
- `url` must be a valid URL format
- `relevance` if present must be between 0 and 1

### ChatSession Validation
- `id` must be a non-empty string
- `messages` must be an array of valid ChatMessage objects
- `isOpen` must be a boolean
- `isLoading` must be a boolean

### SSEData Validation
- `event` must be one of the valid event types ('chunk', 'sources', 'done')
- `data` must be a string

## State Transitions

### Chat Panel State
1. **Closed**: Initial state when widget is just a floating button
2. **Opening**: Transition state when button is clicked
3. **Open**: Chat panel is visible and interactive
4. **Closing**: Transition state when close button is clicked

### Message Status State
1. **Sending**: Message has been submitted but not yet acknowledged by server
2. **Sent**: Message acknowledged by server
3. **Delivered**: Message successfully processed
4. **Error**: Message failed to send

### Loading State
1. **Idle**: No messages being processed
2. **Loading**: Waiting for bot response
3. **Streaming**: Receiving SSE events for bot response
4. **Complete**: Response fully received

## Relationships

### ChatSession → ChatMessage
- One-to-many relationship: Each session contains multiple messages

### ChatMessage → SourceCitation
- One-to-many relationship: Each bot message may reference multiple sources

### ChatMessage → SSEData
- One-to-many relationship: Each bot message may be composed of multiple SSE chunks