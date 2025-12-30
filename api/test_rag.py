"""
Test script to verify the RAG service functionality.
"""
from src.services.rag import retrieve, build_context

def test_rag_service():
    print("Testing RAG service...")

    # Test retrieval with a sample query
    query = "embodied intelligence"
    print(f"Query: {query}")

    results = retrieve(query, top_k=5)
    print(f"Retrieved {len(results)} chunks")

    for i, result in enumerate(results):
        print(f"{i+1}. Score: {result['score']:.4f}, Text: {result['chunk']['text'][:100]}...")

    # Test context building
    context, sources = build_context(results)
    print(f"\nContext length: {len(context)} characters")
    print(f"Number of sources: {len(sources)}")
    print("Sources:")
    for source in sources:
        print(f"  - {source['title']}: {source['url']}")

if __name__ == "__main__":
    test_rag_service()