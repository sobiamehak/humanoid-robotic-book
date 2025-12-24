---
id: 3
title: Create AI Textbook Specification
stage: spec
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: 1-ai-textbook
branch: 1-ai-textbook
user: user
command: /sp.specify
labels: ["spec", "feature-creation"]
links:
  spec: specs/1-ai-textbook/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-ai-textbook/spec.md
  - specs/1-ai-textbook/checklists/requirements.md
tests:

---

## Prompt

```text
Create the complete specification for the AI-native textbook on Physical AI & Humanoid Robotics (Official Panaversity/GIAIC/PIAIC Quarter)

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

This textbook will become the official Panaversity Physical AI resource and the first-ever personalized, Urdu-enabled, RAG-powered humanoid robotics textbook in the world.
```

## Response snapshot

Specification created for 'AI-native textbook on Physical AI & Humanoid Robotics', branch '1-ai-textbook'. All checklist items passed.

## Outcome

- ✅ Impact: Complete feature specification created and validated.
- 🧪 Tests: N/A
- 📁 Files: specs/1-ai-textbook/spec.md and specs/1-ai-textbook/checklists/requirements.md created.
- 🔁 Next prompts: User can now proceed with `/sp.plan`.
- 🧠 Reflection: The spec was successfully created based on detailed user input without needing clarifications. Dependent templates should be updated to align with the new constitution and spec.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
