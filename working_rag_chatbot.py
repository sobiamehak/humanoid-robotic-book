from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient
import openai
from fastapi.middleware.cors import CORSMiddleware
import uuid
from datetime import datetime

# Simple in-memory conversation store (in production, use Redis or database)
conversation_store: Dict[str, List[Dict]] = {}

# Load environment variables from backend directory
load_dotenv(".env")  # Try current directory first
if not os.getenv("COHERE_API_KEY"):
    load_dotenv("backend/.env")  # Try backend directory
if not os.getenv("COHERE_API_KEY"):
    load_dotenv("../backend/.env")  # Try relative path

app = FastAPI(title="Physical AI Humanoid Robotics RAG Chatbot", version="1.0.0")

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*","http://localhost:3000"
                   ,"https://sobiamehak.github.io/humanoid-robotic-book/"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

# Initialize clients (with fallback to CO_API_KEY for Cohere)
cohere_api_key = os.getenv("COHERE_API_KEY") or os.getenv("CO_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY or CO_API_KEY must be set in environment variables")

cohere_client = cohere.Client(cohere_api_key)
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
    session_id: Optional[str] = None  # Add session ID for conversation memory

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
    greetings = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'good night', 'bye']
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
        r'^what\'?s\s+new',
        r'^long\s+time\s+no\s+see',
        r'^nice\s+to\s+meet\s+you'
    ]

    for pattern in greeting_patterns:
        if re.match(pattern, query_lower):
            return True

    # Check if query is very short and doesn't contain question words
    if len(query.split()) <= 2 and not any(word in query_lower for word in [
        'what', 'how', 'why', 'when', 'where', 'who', 'which', 'explain', 'describe',
        'chapter', 'robot', 'ai', 'humanoid', 'physical', 'book', 'topic', 'section',
        'robotics', 'learning', 'system', 'control', 'motion', 'design'
    ]):
        return True

    return False

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    query = request.query.strip()

    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Create or use existing session ID
    session_id = request.session_id or str(uuid.uuid4())

    # Initialize conversation history for this session if it doesn't exist
    if session_id not in conversation_store:
        conversation_store[session_id] = []

    # Handle greetings and off-topic queries
    if is_greeting_or_off_topic(query):
        # Add to conversation history
        conversation_store[session_id].append({
            "role": "user",
            "content": query,
            "timestamp": datetime.now().isoformat()
        })

        if query.lower().strip() in ['hi', 'hello', 'hey', 'greetings']:
            response_text = "Hello! Ask about the Physical AI Humanoid Robotics book."
        else:
            response_text = "Got it! Feel free to ask questions about the Physical AI Humanoid Robotics book."

        # Add to conversation history
        conversation_store[session_id].append({
            "role": "assistant",
            "content": response_text,
            "timestamp": datetime.now().isoformat()
        })

        return ChatResponse(
            query=query,
            response=response_text,
            sources=[]
        )

    try:
        # Generate embedding using Cohere embed-english-light-v3.0
        embed_response = cohere_client.embed(
            texts=[query],
            model="embed-english-light-v3.0",  # Using the specific model that matches your Qdrant vectors
            input_type="search_query"
        )
        query_embedding = embed_response.embeddings[0]

        # Search in Qdrant with limited results to prevent token overflow
        search_results = qdrant_client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_embedding,
            limit=2,  # Reduced from 5 to 2 to limit context size
            score_threshold=None  # No score threshold as requested
        )

        # Format retrieved chunks with aggressive context size limitation
        retrieved_chunks = []
        sources = []
        total_context_length = 0
        max_context_length = 800  # More aggressive limit to prevent token overflow

        for hit in search_results:
            text = hit.payload.get("text", "")
            chapter = hit.payload.get("chapter", "Unknown")
            score = hit.score

            if text:  # Only add if text exists
                # More aggressive text length limiting to prevent any single chunk from being too large
                limited_text = text[:200] + "..." if len(text) > 200 else text
                chunk = f"[Chapter: {chapter}]\n{limited_text}"

                # Check if adding this chunk would exceed the max context length
                if total_context_length + len(chunk) <= max_context_length:
                    retrieved_chunks.append(chunk)
                    sources.append(Source(
                        chapter=chapter,
                        text=text[:100] + "..." if len(text) > 100 else text,
                        score=score
                    ))
                    total_context_length += len(chunk)
                else:
                    # If adding this chunk would exceed the limit, break the loop
                    break

        if not retrieved_chunks:
            context = "No relevant information found in the book."
        else:
            context = "\n\n".join(retrieved_chunks)

        # Build conversation history context
        conversation_history = ""
        if conversation_store[session_id]:
            # Get last 3-4 exchanges to provide context without exceeding token limits
            recent_conversations = conversation_store[session_id][-4:]  # Get last 4 messages (2 exchanges)
            conversation_history = "Previous conversation:\n"
            for msg in recent_conversations:
                role = "User" if msg["role"] == "user" else "Assistant"
                conversation_history += f"{role}: {msg['content']}\n"

        # Generate response using Claude via OpenRouter
        system_message = f"""You are an expert on the Physical AI Humanoid Robotics book (12 chapters).
        Use the previous conversation context if relevant to provide coherent responses.
        Answer ONLY using the provided context. Cite chapters. If not enough info, say so. Never make up facts.
        Keep responses concise and relevant to the question.

        {conversation_history}"""

        prompt = f"""Context information:
        {context}

        Question: {query}

        Please provide a concise, helpful answer to the question based on the context provided. Focus specifically on answering the question asked. If the context does not contain enough information to answer the question, acknowledge this briefly. Limit your response to 2-3 sentences when possible."""

        # Try with the full prompt first
        try:
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
        except Exception as e:
            # If the full context causes a token limit error, try with reduced context
            if "token" in str(e).lower() or "limit" in str(e).lower():
                # Reduce context further by taking only the highest scoring result
                if retrieved_chunks:
                    reduced_context = retrieved_chunks[0]  # Use only the first (highest scoring) chunk
                    reduced_prompt = f"""Context information:
                    {reduced_context}

                    Question: {query}

                    Please provide a concise, helpful answer to the question based on the context provided. Focus specifically on answering the question asked. If the context does not contain enough information to answer the question, acknowledge this briefly. Limit your response to 2-3 sentences when possible."""

                    # Use the same system message that includes conversation history
                    response = openrouter_client.chat.completions.create(
                        model="anthropic/claude-3.5-sonnet",
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": reduced_prompt}
                        ],
                        temperature=0.3,
                        max_tokens=500
                    )
                    llm_response = response.choices[0].message.content
                else:
                    llm_response = "No relevant information found in the book to answer your question."
            else:
                # Re-raise the exception if it's not a token limit error
                raise e

        # Add the current interaction to conversation history
        conversation_store[session_id].append({
            "role": "user",
            "content": query,
            "timestamp": datetime.now().isoformat()
        })
        conversation_store[session_id].append({
            "role": "assistant",
            "content": llm_response,
            "timestamp": datetime.now().isoformat()
        })

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
    return {"status": "healthy", "message": "RAG chatbot is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)  # Use port 8003 to avoid conflicts