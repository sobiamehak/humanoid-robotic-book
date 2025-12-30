---
id: 2
title: "Chatbot API Endpoint Fix"
stage: "general"
date: "2025-12-28"
model: "claude-sonnet-4-5-20250929"
feature: "chat-frontend"
branch: "001-chat-frontend"
user: "claude-code"
command: "Manual fix"
labels: ["bug-fix", "api", "chat-widget", "backend-integration"]
links:
  spec: "specs/001-chat-frontend/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "docs/src/components/ChatWidget/ChatInput.tsx"
tests: []
---

# Chatbot API Endpoint Fix

## Summary
Fixed the chatbot "Service error: The AI service is temporarily unavailable" issue by correcting the API endpoint configuration to use the local backend instead of an external Hugging Face Space endpoint.

## Problem
The ChatWidget component was showing "Service error: The AI service is temporarily unavailable" when users tried to interact with the chatbot. This was caused by incorrect API endpoint configuration.

## Root Cause
The ChatInput component in the ChatWidget was configured to use an external Hugging Face Space endpoint (`https://mehaksobi-my-book.hf.space/api/ask`) instead of the local backend API that was developed for this project.

## Solution
1. Updated the API endpoint in `docs/src/components/ChatWidget/ChatInput.tsx` to use the local `/api/chat` endpoint
2. Restored the proper Server-Sent Events (SSE) streaming implementation that matches the backend API
3. Ensured the request body format matches the backend expectations (message, selected_text, current_page)
4. Maintained proper error handling for various failure scenarios

## Backend API Details
- Endpoint: `POST /api/chat` (with prefix `/api` from the router)
- Supports SSE streaming with 'chunk', 'sources', and 'done' events
- Expects JSON body with: {message: string, selected_text: string | null, current_page: string | null}
- CORS is configured to allow `http://localhost:3000` (Docusaurus frontend)

## Files Modified
- `docs/src/components/ChatWidget/ChatInput.tsx` - Updated API endpoint and restored SSE streaming logic

## Verification
- API endpoint now correctly points to local backend
- SSE streaming implementation matches backend capabilities
- Error handling properly covers network and service errors
- Request format matches backend expectations
- CORS settings already configured for frontend integration