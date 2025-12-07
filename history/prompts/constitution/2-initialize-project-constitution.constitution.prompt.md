---
id: 2
title: Initialize Project Constitution
stage: constitution
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: ["constitution", "initialization"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:

---

## Prompt

```text
project:
  name: "Physical AI & Humanoid Robotics: An AI-Native Textbook"
  description: >
    An interactive, AI-native textbook for teaching Physical AI and Humanoid Robotics using Docusaurus,
    embedded RAG chatbot, user authentication, personalization, and Urdu translation features.
  version: 1.0.0
  type: ai-native-textbook
  domain: physical-ai-humanoid-robotics

core_principles:
  - "Accuracy via up-to-date research and real-world humanoid projects (2024–2025)"
  - "Clarity for advanced undergraduate / graduate CS and robotics students"
  - "Interactivity first: every chapter must be usable by an AI agent and a RAG chatbot"
  - "Personalization and inclusivity (Urdu + background-aware adaptation)"
  - "Reproducibility of all code, simulations, and hardware experiments"

key_standards:
  book_structure: markdown-docusaurus
  citation_style: IEEE
  language_primary: English
  language_secondary: Urdu (on-demand translation)
  reading_level: University sophomore/junior (Flesch-Kincaid 12–14)
  plagiarism_tolerance: 0%
  minimum_sources_per_chapter: 8
  source_preference:
    - 50%+ peer-reviewed (ICRA, IROS, RSS, Science Robotics, Nature Machine Intelligence)
    - 30% official technical reports (Tesla Bot, Boston Dynamics, Figure, Agility Robotics, Unitree, etc.)
    - 20% latest arXiv preprints (2024–2025) from leading labs

deliverables:
  base_100_points:
    - Fully functional Docusaurus site deployed on GitHub Pages
    - Complete textbook (minimum 10 chapters + appendices)
    - Embedded RAG chatbot using:
        backend: FastAPI + Neon Serverless Postgres + Qdrant Cloud (Free Tier)
        frontend: OpenAI Agents SDK / ChatKit
        features:
          - Answer from entire book
          - Answer only from user-selected text
          - Citation of exact section/page

  bonus_up_to_200_points:
    50_points_claude_subagents:
      - Use Claude Code Subagents & Agent Skills during book creation
      - At least 5 reusable skills published in the repo
      - Proof commit history shows heavy use of Claude Code

    50_points_authentication:
      - Signup / Signin using Better Auth[](https://www.better-auth.com/)
      - On signup collect user background
      - Store profile in Neon Postgres

    50_points_personalization:
      - "Personalize this chapter" button at top of every chapter
      - Content adapts based on user profile

    50_points_urdu_translation:
      - "اردو میں ترجمہ کریں" button at top of every chapter
      - Real-time high-quality Urdu translation

book_outline:
  title: "Physical AI & Humanoid Robotics: Building the Future of Embodied Intelligence"
  chapters:
    - 1_Introduction_to_Physical_AI.md
    - 2_Kinematics_Dynamics_Whole_Body_Control.md
    - 3_Actuation_Technologies_2025.md
    - 4_Perception_for_Humanoids.md
    - 5_Locomotion_Bipedal_Walking_Running.md
    - 6_Manipulation_and_Dexterity.md
    - 7_Human_Robot_Interaction_Social_Robotics.md
    - 8_Learning_from_Demonstration_Reinforcement_Learning.md
    - 9_Sim_to_Real_Transfer.md
    - 10_Real_World_Deployments_2025_Case_Studies.md
    - 11_Ethics_Safety_Societal_Impact.md

success_criteria:
  - Live on GitHub Pages
  - All bonus features working
  - Proof of Claude Code subagent usage in git history

mission: "Create the world's first truly interactive, personalized, multilingual AI-native textbook on Physical AI & Humanoid Robotics"
```

## Response snapshot

Constitution updated to version 1.0.0. Manual follow-up needed for various templates.

## Outcome

- ✅ Impact: Project constitution initialized with user-provided details.
- 🧪 Tests: N/A
- 📁 Files: .specify/memory/constitution.md created/modified.
- 🔁 Next prompts: User will be provided with a summary and suggested commit message.
- 🧠 Reflection: The constitution was successfully initialized. Next, update dependent templates.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
