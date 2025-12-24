"""
Initialization script for the RAG chatbot system.
This script will load all textbook content and ingest it into the vector database.
"""
import os
import sys
from pathlib import Path

# Add the backend src directory to the Python path so imports work
backend_src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, backend_src_path)

from src.services.textbook_content_loader import TextbookContentLoader


def initialize_rag_system():
    """
    Initialize the RAG system by loading and ingesting all textbook content
    """
    print("Initializing RAG system with textbook content...")

    # Adjust the docs_path to point to the main project docs directory
    docs_path = Path(__file__).parent.parent.parent / "docs"  # Go up two levels to reach main project

    if not docs_path.exists():
        print(f"Error: Docs directory does not exist at {docs_path}")
        return False

    print(f"Loading content from: {docs_path}")

    # Create the content loader with the correct path
    loader = TextbookContentLoader(docs_path=str(docs_path))

    # Ingest all textbook content
    result = loader.ingest_textbook_content()

    print("\nRAG system initialization completed!")
    print(f"Successful: {result['successful']}")
    print(f"Failed: {result['failed']}")

    if result['errors']:
        print("\nErrors encountered during initialization:")
        for error in result['errors']:
            print(f"  - {error}")
        return False

    print("\nThe RAG chatbot is now ready to answer questions about the textbook content!")
    return True


if __name__ == "__main__":
    success = initialize_rag_system()
    if not success:
        sys.exit(1)  # Exit with error code if initialization failed