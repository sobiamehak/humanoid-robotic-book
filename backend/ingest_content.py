"""
Script to load textbook content and ingest it into the RAG system.
This will process all MD/MDX files in the docs directory and store them in Qdrant.
"""
import sys
import os

# Add the backend src directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from services.textbook_content_loader import TextbookContentLoader


def main():
    print("Starting textbook content ingestion process...")

    # Create the content loader
    loader = TextbookContentLoader()

    # Ingest all textbook content
    result = loader.ingest_textbook_content()

    print("\nIngestion process completed!")
    print(f"Successful: {result['successful']}")
    print(f"Failed: {result['failed']}")

    if result['errors']:
        print("\nErrors encountered:")
        for error in result['errors']:
            print(f"  - {error}")

    print("\nThe RAG system is now ready to answer questions about the textbook content!")


if __name__ == "__main__":
    main()