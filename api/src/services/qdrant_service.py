from qdrant_client import QdrantClient
from src.config.settings import settings
from typing import List, Dict, Any, Optional
import logging


class QdrantService:
    def __init__(self):
        try:
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
            )
            self.is_connected = self.check_connection_sync()
        except Exception as e:
            logging.error(f"Failed to initialize Qdrant client: {e}")
            self.client = None
            self.is_connected = False

    def check_connection_sync(self) -> bool:
        """
        Synchronous check if Qdrant connection is available
        """
        if not self.client:
            return False
        try:
            # Try to get collection info to verify connection
            self.client.get_collections()
            return True
        except Exception as e:
            logging.error(f"Qdrant connection failed: {e}")
            return False

    async def search(self, query_vector: List[float], collection_name: str = "my_book", limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in Qdrant collection
        """
        if not self.client:
            logging.error("Qdrant client not initialized")
            return []

        try:
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit
            )
            return [result.payload for result in results]
        except Exception as e:
            logging.error(f"Error searching Qdrant: {e}")
            return []

    async def check_connection(self) -> bool:
        """
        Check if Qdrant connection is available (async wrapper)
        """
        return self.is_connected