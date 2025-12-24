# Physical AI & Humanoid Robotics Textbook and RAG Chatbot Backend

An AI-native textbook on Physical AI & Humanoid Robotics, developed as part of the Panaversity/GIAIC/PIAIC Quarter project. This comprehensive resource features 13 chapters and 2 appendices covering all aspects of humanoid robotics from fundamentals to advanced topics, with a backend RAG chatbot system for querying book content.

## Main Textbook Features

- **13 Comprehensive Chapters**: Covering robotics fundamentals, locomotion, manipulation, AI, and ethics
- **Interactive RAG Chatbot**: With both full-book and selected-text query modes
- **User Authentication & Profiling**: With personalization based on user background
- **Real-time Urdu Translation**: Instant translation to Urdu for accessibility
- **Personalized Content**: Content adaptation based on user profile
- **Complete Simulation Environment**: With tools for robotics development and testing

## RAG Chatbot Backend Features

- **Multi-Agent Architecture**: Main, Retrieval, and Generation agents for processing queries
- **Qdrant Vector Database**: For efficient content retrieval
- **LLM Integration**: Using OpenRouter API for response generation
- **Off-Topic Query Handling**: Graceful responses for queries outside book scope
- **Complex Query Processing**: Multi-step queries requiring information from multiple chapters

## Technology Stack

- **Frontend**: Docusaurus with React
- **Backend**: FastAPI with Python
- **Database**: Neon Serverless Postgres
- **Vector Store**: Qdrant Cloud (Free Tier)
- **Authentication**: Better Auth
- **AI Services**: GPT-4o for translation and personalization

## Installation

```bash
# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
poetry install
```

## Local Development

### Frontend
```bash
cd frontend
npm start
```

### Backend
```bash
cd backend
poetry run uvicorn src.main:app --reload
```

## Project Structure

```
├── backend/              # FastAPI backend with services
│   ├── src/
│   │   ├── models/       # Database models and Pydantic schemas
│   │   ├── services/     # Business logic services
│   │   └── api/          # API endpoints
├── docs/                 # Textbook content (MDX files)
├── frontend/             # Docusaurus frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Special pages
│   └── docs/             # Textbook chapters
├── src/                  # RAG Chatbot backend source
│   └── rag_chatbot/      # Multi-agent RAG system
│       ├── agents/       # Main, Retrieval, Generation agents
│       ├── tools/        # Retrieval tools
│       ├── models/       # Query models
│       ├── services/     # Qdrant and LLM services
│       └── config/       # Configuration management
└── specs/                # Project specifications
    ├── 1-ai-textbook/    # Main textbook feature specs
    └── 1-book-rag-chatbot-backend/ # RAG chatbot backend specs
```

## Chapter Outline

### Module 1: The Robotic Nervous System (ROS 2)
- Chapter 1: Introduction to Physical AI & Humanoid Robotics
- Chapter 2: The Robotic Nervous System - ROS 2

### Module 2: The Digital Twin (Gazebo & Unity)
- Chapter 3: Digital Twin - Gazebo and Unity

### Module 3: The AI-Robot Brain (NVIDIA Isaac)
- Chapter 4: NVIDIA Isaac Platform
- Chapter 5: Perception for Humanoids
- Chapter 8: Learning from Demonstration and RL
- Chapter 9: Sim-to-Real Transfer

### Module 4: Vision-Language-Action (VLA) & Humanoid Mastery
- Chapter 5: Vision-Language-Action (VLA) Models
- Chapter 6: Humanoid Kinematics and Dynamics
- Chapter 7: Bipedal Locomotion and Balance
- Chapter 8: Dexterous Manipulation
- Chapter 9: Learning from Demonstration and RL
- Chapter 10: Conversational and Social Robotics
- Chapter 11: Ethics, Safety, and Societal Impact

## Appendices
- Appendix A: Recommended Hardware Kits
- Appendix B: Open Source Software Stack

## Deployment

### Frontend to GitHub Pages:
```bash
cd frontend
GIT_USER=<your-username> npm run deploy
```

### Backend to Vercel/Serverless:
Follow Vercel deployment instructions for FastAPI applications.

## Key Functionalities

1. **Interactive RAG Chatbot**: Ask questions about the textbook content with citations
2. **User Profiling**: Sign up with background information for personalization
3. **Content Personalization**: Click "Personalize this chapter" button to adapt content
4. **Urdu Translation**: Instant translation with the "اردو میں ترجمہ کریں" button
5. **Complete Robotics Stack**: Full simulation and development environment

## Cost Management

Total running cost maintained under $15/month using free tiers:
- Neon Serverless Postgres: Free tier
- Qdrant Cloud: Free tier
- GitHub Pages: Free
- Vercel: Free tier for backend

## Project Status

✅ **Complete**: All 200+ bonus points features implemented
✅ **Deployed**: Frontend on GitHub Pages
✅ **Interactive**: All bonus features operational
✅ **AI-Native**: Personalization, translation, and RAG capabilities

For complete project documentation, see the [specification files](./specs/1-ai-textbook/spec.md).
