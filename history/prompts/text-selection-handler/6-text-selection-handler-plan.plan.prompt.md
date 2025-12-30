---
id: 6
title: text-selection-handler-plan
stage: plan
date: 2025-12-27
surface: agent
model: Claude Sonnet 4.5
feature: text-selection-handler
branch: 001-text-selection-handler
user: mehak
command: /sp.plan
labels: ["planning", "frontend", "text-selection", "chatbot", "gemini", "architecture"]
links:
  spec: "specs/001-text-selection-handler/spec.md"
  plan: "specs/001-text-selection-handler/plan.md"
  tasks: null
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-text-selection-handler/plan.md"
  - "specs/001-text-selection-handler/research.md"
  - "specs/001-text-selection-handler/data-model.md"
  - "specs/001-text-selection-handler/contracts/chat-api.yaml"
  - "specs/001-text-selection-handler/quickstart.md"
tests: []
outcome: "Successfully created implementation plan for Text Selection Handler and Additional Features"
evaluation: "Plan includes research findings, architecture, data models, API contracts, and quickstart guide with resolved technology feasibility concerns"
---

# Prompt

```
Concise Implementation Plan

Create TextSelectionHandler
Folder: docs/src/components/TextSelectionHandler/
Files: index.tsx, styles.module.css
Add global mouseup/touchend listeners
On selection (>10 chars): show floating "Ask about this" button near cursor
Click: open chat, set input to selected text, auto-send or focus

Update ChatWidget for Context
Capture current_page = window.location.pathname
On send: include selected_text (from selection or input) and current_page in request body
Clear selection after send

Backend: Full LLM Integration
Create src/services/llm.py
Implement complete system prompt template (with rules, context, current_page, selected_text)
Use OpenAI agents SDK:
Model: gemini-1.5-flash (or gemini-1.5-pro)
Enable streaming

In /api/chat route:
Retrieve → build context/sources (from Part 2)
Call Gemini with full prompt
Stream tokens → SSE chunk events
On end: send sources event + done


Guidance & Navigation
Rely on system prompt to:
Explain selected text in context
Provide direct page
```

# Response

Successfully created implementation plan for Text Selection Handler and Additional Features. The plan includes:

- Research findings resolving the technology feasibility concern (using Google Generative Language SDK instead of OpenAI Agents SDK for Gemini)
- Complete architecture with frontend and backend components
- Data models for TextSelection, ChatRequestContext, NavigationLink, LearningGuidance, and ChatResponseStream
- API contract for the enhanced /api/chat endpoint with text selection support
- Quickstart guide with setup steps and testing procedures

The plan addresses all requirements from the specification and provides a clear path for implementation of the text selection functionality, navigation links, and learning guidance features. The plan resolves the technology feasibility gate by confirming that Google's Generative Language SDK can be used for Gemini integration.