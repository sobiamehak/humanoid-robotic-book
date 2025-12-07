# Research Findings: AI-native textbook on Physical AI & Humanoid Robotics

**Feature Branch**: `1-ai-textbook` | **Date**: 2025-12-04
**Related Spec**: [specs/1-ai-textbook/spec.md](specs/1-ai-textbook/spec.md)
**Related Plan**: [specs/1-ai-textbook/plan.md](specs/1-ai-textbook/plan.md)

## Research Approach

- **Strategy**: Research-concurrent (write → research missing parts → cite → continue)
- **Primary Sources**:
    - Official Panaversity syllabus
    - NVIDIA Isaac documentation
    - ROS 2 Humble/Iron documentation
- **Secondary Sources**:
    - ICRA/IROS/RSS 2023–2025 papers
    - arXiv 2024–2025 preprints from leading labs
    - Official technical reports (Tesla Bot, Boston Dynamics, Figure, Agility Robotics, Unitree, etc.)
- **Citation Style**: IEEE (as defined in project constitution)
- **Citation Management**: Minimum 8 cited sources per chapter, stored in `/references` using Zotero + Better-BibTeX.

## Key Decisions and Rationale

### 1. Citation Style

- **Decision**: IEEE
- **Rationale**: Chosen because robotics conferences (ICRA, IROS, Humanoids) predominantly use IEEE style (95% of the time).
- **Alternatives Considered**: APA, MLA.

### 2. Translation Method

- **Decision**: GPT-4o with caching
- **Rationale**: GPT-4o offers the best Urdu technical accuracy and is the most cost-effective solution when translations are cached.
- **Alternatives Considered**: Google Translate, Claude (specifically Claude 3.5/Opus).

### 3. Personalization Engine

- **Decision**: Structured JSON prompts + function calling
- **Rationale**: A prompt-only approach is faster, cheaper, and significantly easier to debug compared to fine-tuning a small model.
- **Alternatives Considered**: Fine-tuning a small model.

### 4. Vector Chunking Strategy

- **Decision**: 800-token chunks with 200-token overlap, including metadata (chapter, module, difficulty).
- **Tradeoff**: Smaller chunks generally lead to better precision in RAG retrieval but result in higher storage costs and potentially more API calls. The chosen size balances precision with cost-efficiency.
- **Alternatives Considered**: Different chunk sizes and overlap values.

### 5. Authentication Provider

- **Decision**: Better Auth
- **Rationale**: This provider is a mandatory requirement specified by the hackathon rules.
- **Alternatives Considered**: No alternatives were considered due to the explicit constraint.
