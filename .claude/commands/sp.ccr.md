# Claude Code Review (CCR) Start

## Purpose
Initializes a Claude Code Review session with proper context and environment setup.

## Description
This command starts a Claude-assisted code review session, preparing the workspace with:
- Session context initialization
- Prerequisite checks (Node.js, Git, etc.)
- Environment setup for code review tasks

## Parameters
- `sessionName`: Optional name for the review session (default: "default")

## Expected Output
- A confirmation that the CCR session has started
- Information about the project context
- Prerequisites check results
- Path to the session context file

## Example Usage as Prompt
```
ccr start
```

## Context Setup
The command will:
1. Locate the project root directory
2. Create/update session context file
3. Perform prerequisite checks
4. Provide session initialization confirmation

## Files Created/Modified
- `.claude/session-context.json` - Session context information