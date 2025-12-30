# Quickstart Guide: Text Selection Handler

## Overview
This guide explains how to implement and test the Text Selection Handler feature that allows users to select text and get contextual explanations.

## Prerequisites
- Completed Parts 1-3 of the RAG Chatbot (basic chat, retrieval, and frontend integration)
- Access to Google Gemini API with appropriate credentials
- Docusaurus documentation site running

## Setup Steps

### 1. Frontend Implementation
1. Create the TextSelectionHandler component:
   ```
   docs/src/components/TextSelectionHandler/
   ├── index.tsx
   ├── styles.module.css
   └── types.ts
   ```

2. Add global event listeners for text selection detection
3. Implement floating "Ask about this" button display logic
4. Integrate with existing ChatWidget for message handling

### 2. Backend Implementation
1. Install Google Generative Language SDK:
   ```bash
   pip install google-generativeai
   ```

2. Update the `/api/chat` endpoint to handle selected_text and current_page parameters
3. Implement enhanced system prompt with context handling
4. Add streaming support for Gemini responses

### 3. Environment Configuration
Set up the following environment variables:
- `GOOGLE_API_KEY`: Your Google API key for Gemini access
- `QDRANT_URL`: URL for your Qdrant vector database
- `QDRANT_API_KEY`: API key for Qdrant access

## Testing

### Basic Functionality Test
1. Navigate to any documentation page
2. Select a piece of text (at least 10 characters)
3. Verify the "Ask about this" button appears
4. Click the button and verify the chat opens with selected text
5. Send the query and verify contextual response

### Navigation Links Test
1. Ask a question that should include navigation links
2. Verify clickable links appear in the response
3. Click a link and verify it navigates to the correct page

### Performance Test
1. Measure response time for queries with and without selected text
2. Verify response time stays under 3 seconds (p95)
3. Test with multiple concurrent users

## Common Issues and Solutions

### Text Selection Not Working
- Ensure global event listeners are properly attached
- Check that selection length threshold is properly implemented
- Verify the button positioning calculation

### Gemini API Not Responding
- Verify API key is properly configured
- Check that the Google Generative Language SDK is correctly installed
- Ensure the system prompt is properly formatted

### Navigation Links Not Clickable
- Verify the response parsing correctly identifies link patterns
- Check that URL formatting is correct for your Docusaurus site
- Ensure link click handlers are properly attached

## Next Steps
- Implement learning guidance features
- Add analytics for tracking text selection usage
- Optimize performance with caching strategies