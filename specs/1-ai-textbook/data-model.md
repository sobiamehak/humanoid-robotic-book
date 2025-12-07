# Data Model: AI-native textbook on Physical AI & Humanoid Robotics

**Feature Branch**: `1-ai-textbook` | **Date**: 2025-12-04
**Related Spec**: [specs/1-ai-textbook/spec.md](specs/1-ai-textbook/spec.md)
**Related Plan**: [specs/1-ai-textbook/plan.md](specs/1-ai-textbook/plan.md)

## Key Entities

### User

-   **Description**: Represents a reader of the textbook, managing their access, personalized experience, and learning journey.
-   **Attributes**:
    -   `user_id`: Unique identifier for the user (Primary Key).
    -   `email`: User's email address (for authentication via Better Auth).
    -   `password_hash`: Hashed password (managed by Better Auth).
    -   `background_info`: JSONB field storing user's academic level, areas of interest, learning style, etc. (collected during signup).
    -   `personalization_preferences`: JSONB field storing user preferences for content adaptation.
    -   `created_at`: Timestamp of user creation.
    -   `updated_at`: Timestamp of last update.
-   **Relationships**: One-to-one with `PersonalizationProfile` (implicitly, as background_info and personalization_preferences could be part of the User entity or a separate profile entity).

### Chapter/Content Segment

-   **Description**: A granular unit of the textbook content, designed for efficient retrieval by the RAG chatbot and for dynamic adaptation.
-   **Attributes**:
    -   `segment_id`: Unique identifier for the content segment (Primary Key).
    -   `chapter_id`: Identifier linking to the parent chapter.
    -   `module_id`: Identifier linking to the parent module.
    -   `content_text`: The actual text content of the segment.
    -   `content_markdown`: Original Markdown/MDX source of the segment.
    -   `code_snippets`: Array of code blocks within the segment.
    -   `simulation_links`: Array of URLs or references to simulations.
    -   `exercises`: Array of exercise descriptions or links.
    -   `difficulty_level`: Metadata indicating the technical difficulty of the segment.
    -   `keywords`: Array of keywords for searching and personalization.
    -   `vector_embedding`: Vector representation of the content for Qdrant (managed by Qdrant).
    -   `source_citation`: Reference to the original source within the book (e.g., "Chapter X, Section Y").
    -   `created_at`: Timestamp of segment creation/ingestion.
    -   `updated_at`: Timestamp of last update.
-   **Relationships**: Many-to-one with `Chapter` (implicit via chapter_id).

### Chatbot Interaction

-   **Description**: Records user queries to the RAG chatbot and the corresponding responses, including sourcing information.
-   **Attributes**:
    -   `interaction_id`: Unique identifier for the interaction (Primary Key).
    -   `user_id`: Foreign Key to the `User` entity.
    -   `query_text`: The natural language question posed by the user.
    -   `response_text`: The chatbot's generated answer.
    -   `sourced_segments`: Array of `segment_id`s from which the answer was derived.
    -   `source_citations`: Array of exact citations (e.g., "Chapter 2, Page 15") from the `Chapter/Content Segment`.
    -   `context_type`: Enum (`ENTIRE_BOOK`, `SELECTED_TEXT`) indicating the scope of the RAG query.
    -   `selected_text_content`: If `context_type` is `SELECTED_TEXT`, stores the user-selected text.
    -   `interaction_timestamp`: Timestamp of the interaction.
-   **Relationships**: Many-to-one with `User`.

### Translation Cache

-   **Description**: Stores previously generated Urdu translations of content segments to optimize performance and reduce API costs.
-   **Attributes**:
    -   `cache_id`: Unique identifier for the cache entry (Primary Key).
    -   `segment_id`: Foreign Key to the `Chapter/Content Segment` entity (the original English content).
    -   `original_language`: Language of the original content (e.g., 'en').
    -   `translated_language`: Language of the cached translation (e.g., 'ur').
    -   `translated_text`: The cached Urdu translation of the segment.
    -   `translation_engine`: The AI model used for translation (e.g., 'GPT-4o', 'Claude 3.5/Opus').
    -   `created_at`: Timestamp of cache entry creation.
    -   `expires_at`: Optional timestamp for cache invalidation.
-   **Relationships**: Many-to-one with `Chapter/Content Segment`.

### Personalization Profile

-   **Description**: Contains the dynamic profile used to adapt content for a specific user. This entity may be merged with the `User` entity, but conceptually represents the adaptable aspects of a user's learning context.
-   **Attributes**:
    -   `profile_id`: Unique identifier for the profile (Primary Key).
    -   `user_id`: Foreign Key to the `User` entity (if separate).
    -   `dynamic_preferences`: JSONB field, constantly updated based on user interactions, progress, and explicit personalization requests.
    -   `adapted_content_version_meta`: Stores metadata about personalized versions of content (e.g., which content blocks were adapted, for what reason).
    -   `last_adapted_timestamp`: Timestamp of the last content adaptation for this user.
-   **Relationships**: One-to-one with `User` (if implemented as a separate entity).
