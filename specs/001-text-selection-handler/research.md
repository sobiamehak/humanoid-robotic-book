# Research Findings: Text Selection Handler Implementation

## R001: OpenAI Agents SDK with Google Gemini

**Decision**: Use Google Generative Language SDK directly instead of OpenAI Agents SDK for Gemini integration
**Rationale**: The OpenAI Agents SDK is designed for OpenAI models, not Google's Gemini models. Google provides its own Python SDK for Gemini integration that works with streaming and provides better functionality.
**Alternatives considered**:
- OpenAI Agents SDK with Gemini (not officially supported)
- Direct Google Generative Language API calls
- Third-party wrapper libraries

**Implementation approach**: Use the `google-generativeai` Python library which provides proper streaming support for Gemini models.

## R002: Text Selection Detection Best Practices

**Decision**: Implement text selection detection using window event listeners with position tracking
**Rationale**: Using `mouseup` and `touchend` events with `window.getSelection()` provides reliable text selection detection across browsers. Position tracking allows for showing the "Ask about this" button near the selection.
**Alternatives considered**:
- Selection API only (less reliable for position)
- Mutation observers (overkill for this use case)
- Shadow DOM approach (unnecessary complexity)

**Implementation approach**: Add global event listeners and calculate cursor position to display floating button.

## R003: System Prompt for Navigation and Guidance

**Decision**: Extend existing system prompt with specific instructions for navigation links and learning guidance
**Rationale**: The system prompt should include clear instructions for the LLM to generate navigation links when relevant and provide learning guidance based on the textbook content.
**Alternatives considered**:
- Separate prompts for different response types
- Dynamic prompt modification based on query type
- Post-processing of responses to add links

**Implementation approach**: Enhance the system prompt template to include instructions for generating navigation links and learning guidance when appropriate.

## Additional Research: Navigation Link Format

**Decision**: Use structured format for navigation links in responses
**Rationale**: To ensure navigation links are properly formatted and clickable, they need to follow a consistent structure that the frontend can parse and render.
**Format**:
```
[Link Title](relative-path/to/page)
```
or potentially a structured JSON format embedded in the response.

## Additional Research: Performance Optimization

**Decision**: Implement caching and optimized retrieval for faster responses
**Rationale**: To meet the <3s response time target, we need to optimize the retrieval process when handling selected text context.
**Approach**: Cache frequently accessed content and optimize the retrieval pipeline to minimize latency.