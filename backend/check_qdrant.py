import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Load .env (same jo tumhara chatbot use kar raha hai)
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "book-rag-db")

# Connect to Qdrant
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

print("🔗 Connecting to Qdrant Cloud...\n")

# 1. Collection info dekho (dimension, total points)
collection_info = client.get_collection(COLLECTION_NAME)
print("Collection Name:", COLLECTION_NAME)
print("Total Points (Chunks):", collection_info.points_count)
print("Vector Dimension:", collection_info.config.params.vectors.size)
print("Status:", collection_info.status)
print("-" * 50)

# 2. Sample points (chunks) dekho
print("Sample 5 Chunks from Book:\n")

scroll_result = client.scroll(
    collection_name=COLLECTION_NAME,
    limit=5,  # Sirf 5 chunks dikhao
    with_payload=True,  # Text aur chapter dikhao
    with_vectors=False  # Vector na dikhao (bohot lamba hota hai)
)

for point in scroll_result[0]:
    payload = point.payload
    text = payload.get("text", "No text")[:500]  # Pehle 500 characters
    chapter = payload.get("chapter", "Unknown")
    print(f"Chapter: {chapter}")
    print(f"Text Preview: {text}...\n")
    print("-" * 30)

print("✅ Check complete!")