"""
Embeddings service using FastEmbed.

This module provides functionality to generate embeddings for text using FastEmbed
with the BAAI/bge-small-en-v1.5 model which produces 384-dimensional vectors.
"""
from typing import List
from fastembed import TextEmbedding


class EmbeddingService:
    """
    Service class for generating embeddings using FastEmbed.
    """
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        """
        Initialize the embedding service with the specified model.

        Args:
            model_name: Name of the model to use for embeddings
        """
        self.model_name = model_name
        self.embedding_model = TextEmbedding(model_name=model_name)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        # Generate embeddings using FastEmbed
        embeddings = list(self.embedding_model.embed(texts))

        # Convert to list of lists (each inner list contains float values)
        result = []
        for embedding in embeddings:
            result.append([float(val) for val in embedding])

        return result

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text string to embed

        Returns:
            Embedding vector as a list of floats
        """
        return self.embed_texts([text])[0]


# Global instance for easy access
embedding_service = EmbeddingService()


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts using the global embedding service.

    Args:
        texts: List of text strings to embed

    Returns:
        List of embedding vectors (each vector is a list of floats)
    """
    return embedding_service.embed_texts(texts)


def embed_text(text: str) -> List[float]:
    """
    Generate embedding for a single text using the global embedding service.

    Args:
        text: Text string to embed

    Returns:
        Embedding vector as a list of floats
    """
    return embedding_service.embed_text(text)