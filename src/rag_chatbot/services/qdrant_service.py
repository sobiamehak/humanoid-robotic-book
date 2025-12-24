import logging
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from ..config.settings import settings

logger = logging.getLogger(__name__)

class QdrantService:
    """Service class for handling Qdrant vector database operations"""

    def __init__(self):
        """Initialize Qdrant client with configuration from settings"""
        if settings.QDRANT_API_KEY:
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
            )
        else:
            # For local or cloud without API key
            self.client = QdrantClient(url=settings.QDRANT_URL)

        self.collection_name = settings.QDRANT_COLLECTION_NAME
        logger.info(f"QdrantService initialized with collection: {self.collection_name}")

    async def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in the Qdrant collection

        Args:
            query_vector: The vector to search for
            top_k: Number of results to return

        Returns:
            List of matching documents with their payloads
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
            )

            # Format results to return only the payload
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'id': result.id,
                    'payload': result.payload,
                    'score': result.score
                })

            logger.info(f"Found {len(formatted_results)} results for query")
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching in Qdrant: {str(e)}")
            raise

    async def create_collection_if_not_exists(self, vector_size: int = 1536):
        """
        Create the collection if it doesn't exist

        Args:
            vector_size: Size of the vectors to store
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
                )
                logger.info(f"Created collection: {self.collection_name}")
            else:
                logger.info(f"Collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error creating collection in Qdrant: {str(e)}")
            raise

    async def insert_vectors(self, points: List[Dict[str, Any]]):
        """
        Insert vectors into the collection

        Args:
            points: List of points to insert, each with id, vector, and payload
        """
        try:
            # Convert to PointsList format for Qdrant
            qdrant_points = []
            for point in points:
                qdrant_points.append(
                    models.PointStruct(
                        id=point['id'],
                        vector=point['vector'],
                        payload=point['payload']
                    )
                )

            self.client.upsert(
                collection_name=self.collection_name,
                points=qdrant_points
            )
            logger.info(f"Inserted {len(points)} vectors into collection")
        except Exception as e:
            logger.error(f"Error inserting vectors into Qdrant: {str(e)}")
            raise

# Global instance for use in other modules
qdrant_service = QdrantService()