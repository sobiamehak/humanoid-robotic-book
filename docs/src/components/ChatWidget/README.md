# ChatWidget Component

A floating chat widget for the Docusaurus-based documentation site that enables users to interact with the RAG system.

## Features

- Floating chat button in bottom-right corner
- 400x600px chat panel with scrollable message list
- Markdown rendering using react-markdown and remark-gfm
- Source citations with clickable links
- SSE streaming integration with backend API
- Responsive design for mobile devices
- Accessibility features

## Usage

The component is automatically integrated into the site via the Root.tsx theme component and appears on all pages.

## Components

- `index.tsx` - Main ChatWidget component with floating button
- `ChatWindow.tsx` - Chat panel with message display
- `ChatMessage.tsx` - Individual message with markdown rendering
- `ChatInput.tsx` - Input field with SSE streaming support
- `SourceCitations.tsx` - Collapsible source citations
- `ChatWidget.module.css` - Component-specific styles

## API Integration

The component connects to the backend API at `/api/chat` using Server-Sent Events for streaming responses.