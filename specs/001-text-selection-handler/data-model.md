# Data Models: Text Selection Handler

## TextSelection
- **selected_text**: string - the actual selected text
  - Validation: Min length 1 character, max length 10000 characters
  - Required: Yes when selection exists
- **page_context**: string - URL path of page where selection occurred
  - Format: Relative path from site root (e.g., "/chapter-1/introduction")
  - Required: Yes
- **timestamp**: datetime - when selection was made
  - Format: ISO 8601
  - Required: Yes
- **selection_bounds**: object - coordinates of the selection (optional)
  - Properties: start_pos, end_pos (for future highlighting features)

## ChatRequestContext
- **user_message**: string - user's message or query
  - Validation: Min length 1 character, max length 10000 characters
  - Required: Yes
- **selected_text**: string? - selected text from the page (optional)
  - Validation: Max length 10000 characters
  - Required: No
- **current_page**: string? - current page context (optional)
  - Format: Relative path from site root
  - Required: No
- **session_id**: string - user session identifier
  - Format: UUID
  - Required: Yes
- **metadata**: object - additional context information
  - Properties: user_agent, timestamp, referrer

## NavigationLink
- **title**: string - display text for the link
  - Validation: Min length 1, max length 200 characters
  - Required: Yes
- **url**: string - destination URL
  - Format: Relative path from site root
  - Validation: Must be a valid site page
  - Required: Yes
- **relevance_score**: number - how relevant the link is to the query
  - Range: 0.0 to 1.0
  - Required: Yes
- **category**: string - type of link (e.g., "prerequisite", "next", "related")
  - Required: Yes

## LearningGuidance
- **type**: string - type of guidance ("next_step", "overview", "prerequisite", "recommendation")
  - Required: Yes
- **content**: string - the guidance message
  - Validation: Min length 1, max length 1000 characters
  - Required: Yes
- **target_content**: string? - specific content being referenced
  - Required: No
- **confidence**: number - confidence level in the guidance
  - Range: 0.0 to 1.0
  - Required: Yes

## ChatResponseStream
- **event_type**: string - type of event ("chunk", "sources", "done", "navigation", "guidance")
  - Required: Yes
- **data**: string - event payload (format depends on event_type)
  - Required: Yes
- **timestamp**: datetime - when event was generated
  - Required: Yes