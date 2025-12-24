# Quickstart: Book RAG Chatbot Backend

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Git (optional, for version control)

## Setup

1. **Clone or create the project directory**
   ```bash
   mkdir rag-chatbot-backend
   cd rag-chatbot-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install agents qdrant-client cohere python-dotenv asyncio
   ```

4. **Create environment file**
   Create a `.env` file with the following content:
   ```env
   QDRANT_URL=https://3edd413a-51b8-47c1-b749-cae4cb09f488.europe-west3-0.gcp.cloud.qdrant.io:6333
   QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.Cva_t82sZPCvSeuoDkTWyLdsXK6gmBIu1S1kaKLil1g
   QDRANT_COLLECTION_NAME=book-rag-db
   OPENROUTER_API_KEY=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
   COHERE_API_KEY=G6fPCy4HS6YGybeO8HUseNEGIWR8vtlJgAg3BR3x
   MODEL_NAME=anthropic/claude-3.5-sonnet
   ```

5. **Verify Qdrant connection**
   ```python
   from qdrant_client import QdrantClient

   client = QdrantClient(
       url="https://3edd413a-51b8-47c1-b749-cae4cb09f488.europe-west3-0.gcp.cloud.qdrant.io:6333",
       api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.Cva_t82sZPCvSeuoDkTWyLdsXK6gmBIu1S1kaKLil1g"
   )

   # Test connection
   collections = client.get_collections()
   print(collections)
   ```

## Running the Application

1. **Start the chatbot**
   ```bash
   python -m src.rag_chatbot.main
   ```

2. **Interactive mode**
   The application will start in interactive mode where you can enter queries about the book on physical AI humanoid robotics.

3. **Example query**
   ```
   > What are the key components of a humanoid robot's locomotion system?
   ```

## Development

1. **Run tests**
   ```bash
   pytest tests/
   ```

2. **Check code quality**
   ```bash
   # Install additional dev dependencies
   pip install pytest black flake8
   ```

## API Endpoints (if applicable)

- `POST /query` - Submit a query to the RAG system
- `GET /health` - Check system health status

## Troubleshooting

- **Qdrant connection issues**: Verify URL and API key in environment variables
- **OpenRouter API errors**: Check API key validity and rate limits
- **Slow responses**: Verify network connectivity to external services