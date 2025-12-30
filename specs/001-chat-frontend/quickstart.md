# Quickstart Guide: RAG Chatbot Frontend Integration

## Prerequisites
- Node.js 18+ and npm/yarn
- Docusaurus project set up
- Access to RAG backend API with `/api/chat` endpoint
- TypeScript development environment

## Setup

### 1. Install Dependencies
```bash
npm install react-markdown remark-gfm
# If not already installed
npm install react react-dom
```

### 2. Create Component Directory
```bash
mkdir -p docs/src/components/ChatWidget
```

### 3. Component Files Structure
Create the following files in `docs/src/components/ChatWidget/`:
- `index.tsx` - Main ChatWidget component
- `ChatWindow.tsx` - Chat panel component
- `ChatMessage.tsx` - Individual message component
- `ChatInput.tsx` - Input field and send button
- `SourceCitations.tsx` - Source citations component
- `ChatWidget.module.css` - Component styles

## Implementation

### 1. Main Component (index.tsx)
The main component handles the floating button and chat panel visibility state.

### 2. Chat Window (ChatWindow.tsx)
Handles the 400x600px chat panel with message history display.

### 3. Message Component (ChatMessage.tsx)
Renders individual messages with markdown support using react-markdown.

### 4. Input Component (ChatInput.tsx)
Handles user input and submission to backend API.

### 5. Source Citations (SourceCitations.tsx)
Displays collapsible source citations with clickable links.

## Integration

### 1. Add to Layout
Import and add the ChatWidget component to your Docusaurus layout:

```jsx
import ChatWidget from '@site/src/components/ChatWidget';

// In your layout component
<ChatWidget />
```

### 2. API Connection
The component connects to the backend API at `/api/chat` using Server-Sent Events for streaming responses.

## Testing

### 1. Unit Tests
Create tests for each component using Jest and React Testing Library:

```bash
npm test
```

### 2. Manual Testing
1. Start Docusaurus development server
2. Verify floating chat button appears in bottom-right corner
3. Click button to open 400x600px chat panel
4. Send a message and verify it appears in chat history
5. Verify bot response streams in with markdown formatting
6. Check that source citations appear and are clickable

## Configuration

### Styling
The component uses CSS modules for styling. Modify `ChatWidget.module.css` to adjust appearance.

### API Endpoint
Update the API endpoint in the ChatInput component if your backend uses a different path.

## Troubleshooting

### Common Issues
- **SSE not working**: Check that your backend supports Server-Sent Events
- **Markdown not rendering**: Verify react-markdown and remark-gfm are properly installed
- **CORS errors**: Ensure your backend allows requests from your frontend domain
- **Chat not appearing**: Check that the component is properly imported in your layout

### Verification Commands
```bash
# Check dependencies
npm list react-markdown remark-gfm

# Run tests
npm test

# Build and check for errors
npm run build
```