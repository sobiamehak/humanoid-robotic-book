# Feature Specification: AI-native textbook on Physical AI & Humanoid Robotics

**Feature Branch**: `1-ai-textbook`
**Created**: 2025-12-04
**Status**: Draft
**Input**: User description: "Create the complete specification for the AI-native textbook on Physical AI & Humanoid Robotics (Official Panaversity/GIAIC/PIAIC Quarter)

Target audience:
  - Undergraduate & graduate students in CS, Robotics, AI, Electrical Engineering
  - Professionals transitioning to Physical AI / Humanoid Robotics
  - Pakistani & South-Asian learners (Urdu translation = high-impact bonus)

Focus & Theme:
  Embodied Intelligence — Bridging digital AI (LLMs, agents) with the physical world via humanoid robots

Goal of the textbook:
  - Become the official textbook for Panaversity’s Physical AI & Humanoid Robotics quarter
  - Take students from zero to building a fully voice-controlled simulated humanoid robot
  - World’s first truly interactive, personalized, Urdu-capable, RAG-powered robotics textbook

Success criteria (Judges will verify these):
  - 13 chapters + 2 appendices exactly matching the official 4-module syllabus
  - Every chapter contains: theory + Python/ROS 2 code + simulations + exercises
  - Fully working embedded RAG chatbot (whole book + selected-text-only mode)
  - Better Auth login + user profiling at signup
  - “Personalize this chapter” button (adapts content to user background)
  - “اردو میں ترجمہ کریں” button (instant high-quality Urdu translation)
  - Live deployment on GitHub Pages
  - Clear proof of Claude Code Subagents & Skills usage in git history
  - All 200 bonus points features implemented

Constraints (must follow exactly):
  - Frontend: Docusaurus + MDX only
  - Backend: FastAPI + Neon Serverless Postgres + Qdrant Cloud Free Tier
  - Auth: Better Auth only[](https://www.better-auth.com/)
  - RAG Frontend: OpenAI ChatKit / Agents SDK
  - Translation & Personalization: GPT-4o or Claude 3.5/Opus (cached in Qdrant/Neon)
  - Total running cost < $15/month (free tiers only)
  - All content in /docs as Markdown/MDX

Not building / Not including:
  - Full cloud lab setup guide
  - Detailed hardware assembly manuals beyond kit recommendations
  - Vendor vs vendor humanoid comparisons
  - ROS 2 from absolute zero (assumes basic Python knowledge)

Chapter outline — Exactly aligned with the official 4 modules:

Module 1: The Robotic Nervous System (ROS 2)
  01_Introduction_to_Physical_AI.md
  02_The_Robotic_Nervous_System_ROS2.md

Module 2: The Digital Twin (Gazebo & Unity)
  03_Digital_Twin_Gazebo_and_Unity.md

Module 3: The AI-Robot Brain (NVIDIA Isaac)
  04_NVIDIA_Isaac_Platform.md
  09_Perception_for_Humanoids.md
  11_Sim_to_Real_Transfer.md

Module 4: Vision-Language-Action (VLA) & Humanoid Mastery
  05_Vision_Language_Action_VLA_Models.md
  06_Humanoid_Kinematics_and_Dynamics.md
  07_Bipedal_Locomotion_and_Balance.md
  08_Dexterous_Manipulation.md
  10_Learning_from_Demonstration_and_RL.md
  12_Conversational_and_Social_Robotics.md
  13_Ethics_Safety_and_Societal_Impact.md

Appendices:
  Appendix_A_Recommended_Hardware_Kits.md      → Jetson + RealSense + Unitree options with exact prices
  Appendix_B_Open_Source_Software_Stack.md     → Complete stack + installation one-liners

Timeline:
  Fully completed & deployed before hackathon deadline → targeting Top 1–3 position

Final Deliverables:
  - Live GitHub Pages URL
  - Public GitHub repo with full Claude Code commit history
  - 5–8 min demo video showing: signup → personalize → Urdu → RAG (selected text)
  - Zero plagiarism + publication-ready quality

This textbook will become the official Panaversity Physical AI resource and the first-ever personalized, Urdu-enabled, RAG-powered humanoid robotics textbook in the world."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Read Textbook Chapters (Priority: P1)

Users can navigate through 13 core chapters and 2 appendices, each containing theoretical concepts, Python/ROS 2 code examples, simulations, and exercises, to learn Physical AI & Humanoid Robotics.

**Why this priority**: Core educational value; fundamental interaction.

**Independent Test**: Can be fully tested by navigating all chapters and verifying content presence (text, code, simulations, exercises) and delivers comprehensive learning material.

**Acceptance Scenarios**:

1. **Given** a user is on the textbook website, **When** they select a chapter, **Then** the chapter content, including theory, code, simulations, and exercises, is displayed.
2. **Given** a user is viewing a chapter, **When** they navigate to an appendix, **Then** the appendix content is displayed.

---

### User Story 2 - Interact with RAG Chatbot (Priority: P1)

Users can ask questions to an embedded RAG chatbot, receiving answers sourced either from the entire textbook or specifically from user-selected text, with exact citations.

**Why this priority**: Enhances interactivity and personalized learning; critical bonus feature.

**Independent Test**: Can be fully tested by posing questions to the chatbot (both general and context-specific) and verifying accurate, cited responses, delivering immediate knowledge access.

**Acceptance Scenarios**:

1. **Given** a user is viewing any part of the book, **When** they ask a question to the RAG chatbot, **Then** the chatbot provides an answer from the entire book, citing the source.
2. **Given** a user selects a specific text segment, **When** they ask a question to the RAG chatbot, **Then** the chatbot provides an answer only from the selected text, citing the exact section/page.

---

### User Story 3 - User Authentication & Profiling (Priority: P2)

New users can sign up using Better Auth, providing background information, while existing users can sign in, enabling personalization features.

**Why this priority**: Essential for personalization and tracking; high-impact bonus feature.

**Independent Test**: Can be fully tested by successfully registering a new account, logging in, and verifying that user background information is collected and stored, delivering a secure and personalized experience.

**Acceptance Scenarios**:

1. **Given** a new user wants to access personalized content, **When** they sign up via Better Auth, **Then** their account is created, and their background information is collected and stored.
2. **Given** an existing user wants to access personalized content, **When** they sign in via Better Auth, **Then** they are successfully authenticated.

---

### User Story 4 - Personalize Chapter Content (Priority: P2)

Users can click a "Personalize this chapter" button, and the chapter content dynamically adapts based on their previously provided background information.

**Why this priority**: Delivers on the core promise of an AI-native, personalized textbook; high-impact bonus feature.

**Independent Test**: Can be fully tested by setting different user profiles, then accessing a chapter and verifying that the content changes to reflect the specified background, delivering tailored learning.

**Acceptance Scenarios**:

1. **Given** a logged-in user with a specific background views a chapter, **When** they click "Personalize this chapter", **Then** the chapter content is adapted to their background.

---

### User Story 5 - Urdu Translation (Priority: P2)

Users can click an "اردو میں ترجمہ کریں" button to receive a real-time, high-quality Urdu translation of the current chapter.

**Why this priority**: Addresses inclusivity for Pakistani & South-Asian learners; high-impact bonus feature.

**Independent Test**: Can be fully tested by viewing a chapter, clicking the Urdu translation button, and verifying that the chapter content is accurately and fluently translated into Urdu, delivering multilingual accessibility.

**Acceptance Scenarios**:

1. **Given** a user is viewing a chapter, **When** they click "اردو میں ترجمہ کریں", **Then** the chapter content is translated into high-quality Urdu.

---

### Edge Cases

- What happens when a user attempts to access personalized content without logging in or providing background information? (System should prompt login/profile completion.)
- How does the system handle very long chapters or complex technical terms during real-time translation and personalization? (Ensure performance and accuracy).
- What happens if the RAG chatbot cannot find a relevant answer in the book? (Graceful fallback, suggest alternative searching).
- How does the system ensure the total running cost remains under $15/month with all features active? (Monitoring and optimization of free tiers).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The Docusaurus site MUST be fully functional and deployed on GitHub Pages.
- **FR-002**: The textbook MUST contain 13 chapters and 2 appendices, precisely matching the official 4-module syllabus.
- **FR-003**: Each chapter MUST include theoretical explanations, Python/ROS 2 code, simulations, and exercises.
- **FR-004**: The system MUST embed a RAG chatbot with a FastAPI backend, Neon Serverless Postgres, and Qdrant Cloud (Free Tier).
- **FR-005**: The RAG chatbot frontend MUST use OpenAI ChatKit or Agents SDK.
- **FR-006**: The RAG chatbot MUST be able to answer questions from the entire book content.
- **FR-007**: The RAG chatbot MUST be able to answer questions only from user-selected text segments.
- **FR-008**: The RAG chatbot MUST provide citations to the exact section/page for its answers.
- **FR-009**: The system MUST implement user signup and signin functionality using Better Auth (https://www.better-auth.com/).
- **FR-010**: The system MUST collect user background information during the signup process.
- **FR-011**: The system MUST store user profiles, including background information, in Neon Postgres.
- **FR-012**: Each chapter page MUST include a "Personalize this chapter" button.
- **FR-013**: Chapter content MUST adapt dynamically based on the logged-in user's profile and background.
- **FR-014**: Each chapter page MUST include an "اردو میں ترجمہ کریں" button.
- **FR-015**: The system MUST provide real-time, high-quality Urdu translation of chapter content upon request.
- **FR-016**: Translation and personalization services MUST utilize GPT-4o or Claude 3.5/Opus, with results cached in Qdrant or Neon for efficiency.
- **FR-017**: All textbook content MUST reside in the `/docs` directory as Markdown/MDX files.
- **FR-018**: The total running cost of all deployed services MUST remain under $15/month, leveraging free tiers where possible.
- **FR-019**: The system MUST generate a public GitHub repository with a full Claude Code commit history.
- **FR-020**: The system MUST produce a 5–8 minute demo video showcasing signup, personalization, Urdu translation, and RAG (selected text).
- **FR-021**: The final textbook content MUST exhibit zero plagiarism and be of publication-ready quality.

### Key Entities *(include if feature involves data)*

- **User**: Represents a reader of the textbook. Attributes include authentication credentials, background information (e.g., academic level, areas of interest), and personalization preferences.
- **Chapter/Content Segment**: Represents a distinct section of the textbook. Attributes include text, code, simulation links, exercises, and metadata for RAG retrieval and citation.
- **Chatbot Interaction**: Represents a user's query and the chatbot's response. Attributes include query text, response text, source citations, and context (entire book or selected text).
- **Translation Cache**: Stores previously translated segments to reduce API calls and improve performance.
- **Personalization Profile**: Stores the user's background and preferences used to adapt content.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The deployed Docusaurus site is accessible via a live GitHub Pages URL.
- **SC-002**: All 13 chapters and 2 appendices are fully present and accurately align with the 4-module syllabus.
- **SC-003**: Every chapter is verified to contain theory, Python/ROS 2 code, simulations, and exercises.
- **SC-004**: The embedded RAG chatbot is fully functional, capable of answering from the entire book and user-selected text, with accurate citations.
- **SC-005**: User signup and signin via Better Auth are fully operational, with user background successfully collected and stored.
- **SC-006**: The "Personalize this chapter" button dynamically adapts chapter content based on user profiles as demonstrated in the demo video.
- **SC-007**: The "اردو میں ترجمہ کریں" button provides instant, high-quality Urdu translation of chapter content as demonstrated in the demo video.
- **SC-008**: The total monthly running cost of all deployed services remains below $15, verified through billing dashboards.
- **SC-009**: Git history provides clear evidence of extensive Claude Code Subagent and Agent Skills usage during development.
- **SC-010**: The project successfully achieves all 200 bonus points as defined in the project brief.
