from qdrant_client import QdrantClient
from src.config.settings import settings

try:
    # Connect to Qdrant
    client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)

    # Test the connection by getting collections
    collections = client.get_collections()
    print("SUCCESS: Qdrant connection successful!")
    print(f"Available collections: {[c.name for c in collections.collections]}")

except Exception as e:
    print(f"ERROR: Qdrant connection failed: {e}")