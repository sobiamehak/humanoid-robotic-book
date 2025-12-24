import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Configuration settings for the RAG chatbot backend"""

    # Qdrant Configuration
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")

    # LLM Configuration (OpenRouter or other)
    LLM_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")

    # Cohere Configuration (if needed)
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Model Configuration
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "openai/gpt-3.5-turbo")

    # Database Configuration
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "book_content")

# Create a global settings instance
settings = Settings()