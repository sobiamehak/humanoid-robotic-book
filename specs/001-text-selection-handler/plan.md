# Implementation Plan: Text Selection Handler and Additional Features

**Feature**: Text Selection Handler and Additional Features
**Branch**: 001-text-selection-handler
**Created**: 2025-12-27
**Status**: Draft
**Input**: User requirements from spec.md

## Technical Context

**Frontend Components**:
- TextSelectionHandler component to detect text selection and show "Ask about this" button
- Integration with existing ChatWidget for display and streaming
- Components placed under `docs/src/components/TextSelectionHandler/`

**Backend Services**:
- LLM integration using Google Generative Language SDK with Gemini models
- Updated system prompt to handle selected text and current page context
- Streaming responses via SSE

**Technology Stack**:
- Frontend: React/TypeScript with Docusaurus
- Backend: Python with FastAPI
- LLM: Google Gemini via Google Generative Language SDK
- Vector DB: Qdrant (from previous parts)
- Streaming: Server-Sent Events (SSE)

**Unknowns**:
- Exact implementation details of Google Generative Language SDK with Gemini (RESOLVED in research.md)
- How to properly structure the system prompt for guidance/navigation (RESOLVED in research.md)
- Specific format for navigation links in responses (RESOLVED in research.md)

## Constitution Check

- ✅ **Maintainability**: Plan includes modular components with clear separation of concerns
- ✅ **Performance**: Plan accounts for <3s response time and 10+ concurrent users
- ✅ **User Experience**: Plan prioritizes intuitive text selection and contextual help
- ⚠️ **Dependencies**: Plan relies on external Gemini API via Google Generative Language SDK - need to verify availability and costs

## Gates

- [x] **Technology Feasibility**: Google Generative Language SDK supports Gemini integration (RESOLVED in research.md)
- [ ] **Performance Requirements**: Confirm architecture can meet <3s response time targets
- [ ] **Security**: Ensure selected text handling doesn't expose sensitive information
- [ ] **Compatibility**: Verify integration with existing ChatWidget components

---

## Phase 0: Research & Discovery

### Research Tasks

**R001**: Research Google Generative Language SDK integration with Google Gemini models
- Task: "Research how to use Google Generative Language SDK with Gemini models (gemini-1.5-flash/gemini-1.5-pro)"
- Rationale: Need to understand implementation approach for LLM integration
- Status: COMPLETED - See research.md for findings

**R002**: Research best practices for text selection detection in web applications
- Task: "Find best practices for text selection handling with mouseup/touchend events"
- Rationale: Need to implement reliable text selection detection
- Status: COMPLETED - See research.md for findings

**R003**: Research system prompt engineering for navigation and guidance features
- Task: "Research how to structure system prompts for navigation links and learning guidance"
- Rationale: Need to ensure responses include proper navigation and guidance
- Status: COMPLETED - See research.md for findings

### Expected Outcomes
- Clear understanding of Google Generative Language SDK with Gemini
- Verified approach for text selection detection
- Proper system prompt structure for guidance features

---

## Phase 1: Architecture & Design

### Component Architecture

**Frontend Components**:
```
docs/src/components/TextSelectionHandler/
├── index.tsx              # Main TextSelectionHandler component
├── styles.module.css      # CSS module for styling
└── types.ts               # TypeScript types for selection events
```

**Backend Services**:
```
src/services/
├── llm.py                 # LLM integration with Google Generative Language SDK
├── text_selection_handler.py  # Text selection context handling
└── navigation_generator.py    # Navigation link generation
```

### API Contracts

**POST /api/chat** (Enhanced)
- Request body includes:
  - `message`: user message
  - `selected_text`: text selected by user (optional)
  - `current_page`: current page URL path (optional)
- Response: Server-Sent Events stream with:
  - `chunk` events: response tokens
  - `sources` events: citation sources
  - `done` events: completion marker

### Data Models

**TextSelection**:
- `selected_text`: string - the actual selected text
- `page_context`: string - URL path of page where selection occurred
- `timestamp`: datetime - when selection was made

**ChatRequestContext**:
- `user_message`: string - user's message
- `selected_text`: string? - selected text (if any)
- `current_page`: string? - current page context
- `session_id`: string - user session identifier

**NavigationLink**:
- `title`: string - display text for the link
- `url`: string - destination URL
- `relevance_score`: number - how relevant the link is to the query

---

## Phase 2: Implementation Approach

### Sprint 1: Frontend Text Selection
1. Create TextSelectionHandler component
2. Implement text selection detection with mouseup/touchend
3. Add floating "Ask about this" button
4. Integrate with existing ChatWidget

### Sprint 2: Backend LLM Integration
1. Set up OpenAI Agents SDK with Gemini
2. Create enhanced system prompt with selection/page context
3. Update /api/chat endpoint to handle selection context
4. Implement streaming response with SSE

### Sprint 3: Guidance & Navigation
1. Enhance system prompt for navigation links
2. Implement navigation link generation in responses
3. Add learning guidance capabilities
4. Test end-to-end functionality

### Risk Mitigation
- **RISK**: Google Generative Language SDK integration may have unexpected issues
  - **MITIGATION**: Thorough testing with different Gemini models and proper error handling
- **RISK**: Performance targets not met with new features
  - **MITIGATION**: Implement caching and optimize retrieval pipeline
- **RISK**: Text selection conflicts with existing page functionality
  - **MITIGATION**: Thorough testing across different page types

## Dependencies & Integration Points

- **Depends on**: Existing ChatWidget components (from Parts 1-3)
- **Integrates with**: Qdrant vector database (from Part 2)
- **External API**: Google Gemini via Google Generative Language SDK
- **Docusaurus**: Integration via theme components

## Success Criteria for Implementation

- Text selection detection works reliably across all documentation pages
- "Ask about this" button appears appropriately and functions correctly
- Selected text context is properly passed to backend and affects responses
- Navigation links appear in responses when relevant
- Learning guidance is provided in responses when appropriate
- Performance targets (<3s response time) are maintained
- All existing ChatWidget functionality continues to work