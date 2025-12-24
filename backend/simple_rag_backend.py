from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient
import openai

# Load environment variables
load_dotenv()

app = FastAPI(title="Simple RAG Chatbot", version="1.0.0")

# Initialize services
cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
openrouter_client = openai.OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "book-rag-db")

class ChatRequest(BaseModel):
    query: str

class Source(BaseModel):
    chapter: str
    text: str
    score: float

class ChatResponse(BaseModel):
    query: str
    response: str
    sources: List[Source]

def is_greeting_or_off_topic(query: str) -> bool:
    """Check if the query is a greeting or off-topic."""
    query_lower = query.lower().strip()
    greetings = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'good night']
    simple_responses = ['yes', 'no', 'maybe', 'ok', 'okay', 'sure', 'thanks', 'thank you', 'please']

    if query_lower in greetings or query_lower in simple_responses:
        return True

    # Check for greeting-like patterns
    import re
    greeting_patterns = [
        r'^(hi|hello|hey|greetings)\s*(there|there!|!)?$',
        r'^good\s+(morning|afternoon|evening|night)',
        r'^(what\'s|whats)\s+up',
        r'^how\s+are\s+you',
        r'^howdy',
        r'^what\'?s\s+new'
    ]

    for pattern in greeting_patterns:
        if re.match(pattern, query_lower):
            return True

    # Check if query is very short and doesn't contain question words
    if len(query.split()) <= 2 and not any(word in query_lower for word in [
        'what', 'how', 'why', 'when', 'where', 'who', 'which', 'explain', 'describe',
        'chapter', 'robot', 'ai', 'humanoid', 'physical', 'book', 'topic', 'section'
    ]):
        return True

    return False

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    query = request.query.strip()

    # Handle greetings and off-topic queries
    if is_greeting_or_off_topic(query):
        if query.lower().strip() in ['hi', 'hello', 'hey', 'greetings']:
            return ChatResponse(
                query=query,
                response="Hello! Ask about the Physical AI Humanoid Robotics book.",
                sources=[]
            )
        else:
            return ChatResponse(
                query=query,
                response="Got it! Feel free to ask questions about the Physical AI Humanoid Robotics book.",
                sources=[]
            )

    try:
        # Generate embedding using Cohere
        embed_response = cohere_client.embed(
            texts=[query],
            model="embed-english-light-v3.0",  # Using the specific model requested
            input_type="search_query"
        )
        query_embedding = embed_response.embeddings[0]

        # Search in Qdrant with no score threshold
        search_results = qdrant_client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_embedding,
            limit=5,
            score_threshold=None  # No score threshold as requested
        )

        # Format retrieved chunks
        retrieved_chunks = []
        sources = []

        for hit in search_results:
            text = hit.payload.get("text", "")
            chapter = hit.payload.get("chapter", "Unknown")
            score = hit.score

            retrieved_chunks.append(f"[Chapter: {chapter}]\n{text}")
            sources.append(Source(chapter=chapter, text=text[:200] + "..." if len(text) > 200 else text, score=score))

        if not retrieved_chunks:
            context = "No relevant information found in the book."
        else:
            context = "\n\n".join(retrieved_chunks)

        # Generate response using Claude via OpenRouter
        system_message = """You are an expert on the Physical AI Humanoid Robotics book.
        Answer ONLY using the provided context. Cite chapters. If not enough info, say so. Never make up facts."""

        prompt = f"""Context information:
        {context}

        Question: {query}

        Please provide a concise, helpful answer to the question based on the context provided. Focus specifically on answering the question asked. If the context does not contain enough information to answer the question, acknowledge this briefly."""

        response = openrouter_client.chat.completions.create(
            model="anthropic/claude-3.5-sonnet",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )

        llm_response = response.choices[0].message.content

        return ChatResponse(
            query=query,
            response=llm_response,
            sources=sources
        )

    except Exception as e:
        print(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Simple RAG backend is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003
                
                
                )