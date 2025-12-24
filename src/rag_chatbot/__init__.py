import logging
import sys
from .config.settings import settings

# Set up basic logging configuration
def setup_logging():
    """Set up logging configuration for the application"""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('rag_chatbot.log')
        ]
    )

# Call setup_logging when the module is imported
setup_logging()

# Import main components to make them available at package level
from .services.qdrant_service import qdrant_service
from .services.llm_service import llm_service
from .services.query_relevance_service import query_relevance_service
from .config.settings import settings

__version__ = "0.1.0"
__author__ = "Book RAG Chatbot Team"

# Define what gets imported with "from rag_chatbot import *"
__all__ = [
    "qdrant_service",
    "llm_service",
    "query_relevance_service",
    "settings",
    "rag_chatbot_system",
    "setup_logging"
]