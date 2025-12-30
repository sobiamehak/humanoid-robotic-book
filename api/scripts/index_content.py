"""
Indexer script for populating the Qdrant collection with textbook content.

This script processes markdown files from the docs directory, chunks them using
the chunker utility, generates embeddings using the embeddings service,
and upserts them to the Qdrant collection.
"""
import os
from pathlib import Path
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from src.config.settings import settings
from src.services.utils.chunker import chunk_multiple_files
from src.services.embeddings import embed_texts


def get_phase_1_file_paths(docs_dir: str = "docs") -> List[str]:
    """
    Define the file paths for Phase 1 content to be indexed.

    Args:
        docs_dir: Directory containing the documentation

    Returns:
        List of file paths to process
    """
    file_paths = []

    # Add overview file
    file_paths.append(os.path.join(docs_dir, "overview.md"))

    # Add all lesson files from chapters 01-03
    for chapter_num in range(1, 4):  # Chapters 1, 2, 3
        chapter_dir = os.path.join(docs_dir, f"chapter-{chapter_num:02d}")
        if os.path.exists(chapter_dir):
            for file_name in os.listdir(chapter_dir):
                if file_name.endswith(".md"):
                    file_paths.append(os.path.join(chapter_dir, file_name))

    # Also add the main chapter files that might exist in the root docs directory
    for chapter_num in range(1, 4):
        chapter_file = os.path.join(docs_dir, f"chapter-{chapter_num:02d}-*.md")
        # We'll also check for files that match the pattern in the root
        import glob
        matching_files = glob.glob(chapter_file)
        for file_path in matching_files:
            if file_path not in file_paths:
                file_paths.append(file_path)

    # Add the chapter files that were copied from the root docs
    for chapter_num in range(1, 14):  # All chapters 1-13
        chapter_file = os.path.join(docs_dir, f"chapter-{chapter_num:02d}-*.md")
        import glob
        matching_files = glob.glob(chapter_file)
        for file_path in matching_files:
            if file_path not in file_paths:
                file_paths.append(file_path)

    return file_paths


def index_content(collection_name: str = "textbook_content"):
    """
    Main function to index content into Qdrant.

    Args:
        collection_name: Name of the Qdrant collection to create/populate
    """
    print(f"Starting content indexing for collection: {collection_name}")

    # Initialize Qdrant client
    client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)

    # Check if collection exists, create if it doesn't
    collection_exists = False
    try:
        client.get_collection(collection_name)
        collection_exists = True
        print(f"Collection '{collection_name}' already exists")
    except:
        print(f"Creating new collection '{collection_name}'")
        # Create collection with 384-dimensional vectors (for BAAI/bge-small model)
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
        )
        print(f"Collection '{collection_name}' created successfully")

    # Get file paths for Phase 1
    file_paths = get_phase_1_file_paths()
    print(f"Found {len(file_paths)} files to process:")
    for path in file_paths:
        print(f"  - {path}")

    # Process files into chunks
    print("Processing files into chunks...")
    all_chunks = chunk_multiple_files(file_paths)
    print(f"Generated {len(all_chunks)} chunks")

    if not all_chunks:
        print("No chunks generated. Exiting.")
        return

    # Extract texts for embedding
    texts = [chunk["text"] for chunk in all_chunks]

    # Generate embeddings
    print("Generating embeddings...")
    embeddings = embed_texts(texts)
    print(f"Generated {len(embeddings)} embeddings")

    # Prepare points for upsert
    points = []
    for i, (chunk, embedding) in enumerate(zip(all_chunks, embeddings)):
        point = models.PointStruct(
            id=i,
            vector=embedding,
            payload={
                "text": chunk["text"],
                "metadata": chunk["metadata"],
                "source_file": chunk["metadata"]["file_path"]
            }
        )
        points.append(point)

    # Upsert points to Qdrant
    print(f"Upserting {len(points)} points to Qdrant...")
    client.upsert(
        collection_name=collection_name,
        points=points
    )
    print(f"Successfully upserted {len(points)} points")

    # Print summary
    collection_info = client.get_collection(collection_name)
    print(f"\nIndexing complete!")
    print(f"Collection: {collection_name}")
    print(f"Total points: {collection_info.points_count}")
    print(f"Vector size: {collection_info.config.params.vectors.size}")
    print(f"Distance: {collection_info.config.params.vectors.distance}")


if __name__ == "__main__":
    index_content()