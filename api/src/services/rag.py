"""
RAG (Retrieval Augmented Generation) service.

This module provides functionality to retrieve relevant content from indexed documents
based on user queries and build context for the LLM to generate responses.
"""
from typing import List, Dict, Any, Tuple
from qdrant_client import QdrantClient
from ..config.settings import settings
from .embeddings import embed_text
from .utils.chunker import load_markdown_file


class RAGService:
    """
    Service class for RAG functionality - retrieval and context building.
    """
    def __init__(self, collection_name: str = "textbook_content"):
        """
        Initialize the RAG service.

        Args:
            collection_name: Name of the Qdrant collection to search in
        """
        self.collection_name = collection_name
        self.client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve the most relevant chunks for a given query.

        Args:
            query: The user query to search for
            top_k: Number of top results to return

        Returns:
            List of dictionaries containing the retrieved chunks with scores
        """
        # Generate embedding for the query
        query_embedding = embed_text(query)

        # Search in Qdrant
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k
        )

        # Process results
        results = []
        for hit in search_results:
            results.append({
                "chunk": {
                    "id": hit.id,
                    "text": hit.payload.get("text", ""),
                    "metadata": hit.payload.get("metadata", {})
                },
                "score": hit.score,
                "vector": hit.vector
            })

        return results

    def build_context(self, hits: List[Dict[str, Any]]) -> Tuple[str, List[Dict[str, str]]]:
        """
        Build context string from retrieved hits and extract sources.

        Args:
            hits: List of retrieved hits from the retrieve method

        Returns:
            Tuple of (context string, list of sources with title and URL)
        """
        context_parts = []
        sources = []

        for hit in hits:
            chunk = hit["chunk"]
            text = chunk["text"]
            metadata = chunk["metadata"]

            # Add the chunk text to context
            context_parts.append(text)

            # Extract source information
            source_info = {
                "title": metadata.get("section_title", "Unknown Section"),
                "url": metadata.get("source_url", "")
            }
            if source_info not in sources:  # Avoid duplicates
                sources.append(source_info)

        # Join all context parts
        context = "\n\n".join(context_parts)

        return context, sources


# Global instance for easy access
rag_service = RAGService()


def retrieve(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve the most relevant chunks for a given query.

    Args:
        query: The user query to search for
        top_k: Number of top results to return

    Returns:
        List of dictionaries containing the retrieved chunks with scores
    """
    return rag_service.retrieve(query, top_k)


def build_context(hits: List[Dict[str, Any]]) -> Tuple[str, List[Dict[str, str]]]:
    """
    Build context string from retrieved hits and extract sources.

    Args:
        hits: List of retrieved hits from the retrieve method

    Returns:
        Tuple of (context string, list of sources with title and URL)
    """
    return rag_service.build_context(hits)