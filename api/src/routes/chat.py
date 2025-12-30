from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from sse_starlette.sse import EventSourceResponse
import asyncio
import json
from ..services.rag import retrieve, build_context
from ..services.llm_service import LLMService
from ..services.local_response_service import generate_response as generate_local_response


class ChatRequest(BaseModel):
    message: str
    selected_text: Optional[str] = None
    current_page: Optional[str] = None


router = APIRouter()

# Initialize services
llm_service = LLMService()


async def chat_stream(message: str, selected_text: Optional[str] = None, current_page: Optional[str] = None):
    """Streaming response for the chat endpoint with RAG functionality"""
    try:
        # Send initial processing message
        yield {"event": "chunk", "data": "Processing your request..."}

        # Check if the query is off-topic before processing
        off_topic_response = check_off_topic_query(message)
        if off_topic_response:
            # Send empty sources since it's off-topic
            yield {"event": "sources", "data": "[]"}
            # Send off-topic response directly
            response_text = off_topic_response
        else:
            # Retrieve relevant content using RAG service
            hits = retrieve(message, top_k=5)
            context, sources = build_context(hits)

            # Send the sources event with real source information
            # Ensure proper JSON serialization
            sources_json = json.dumps(sources, ensure_ascii=False)
            yield {"event": "sources", "data": sources_json}

            # Generate response using LLM with retrieved context
            full_context = context
            if selected_text:
                full_context += f"\n\nSelected text: {selected_text}"
            if current_page:
                full_context += f"\n\nCurrent page content: {current_page}"

            # Try to generate response with LLM service (OpenRouter/Gemini), with fallback to local service
            try:
                response_text = await llm_service.generate_response(message, full_context)
                # Check if the response indicates an error
                if "Sorry, I encountered an error" in response_text or "encountered an error" in response_text:
                    print("LLM service returned an error, using local response as fallback")
                    response_text = generate_local_response(message, full_context)
            except Exception as llm_error:
                # If LLM service throws an exception, use local response service as fallback
                print(f"LLM service failed: {llm_error}")
                response_text = generate_local_response(message, full_context)

        # Stream the response in chunks
        words = response_text.split()
        for i, word in enumerate(words):
            if i == 0:
                yield {"event": "chunk", "data": word}
            else:
                yield {"event": "chunk", "data": f" {word}"}

        # Send done event
        yield {"event": "done", "data": "true"}

    except Exception as e:
        print(f"Chat stream error: {e}")
        # Use local response as ultimate fallback when there's an error
        try:
            # Retrieve context again in case of error
            hits = retrieve(message, top_k=3)
            context, sources = build_context(hits)

            # Send sources event
            # Ensure proper JSON serialization
            sources_json = json.dumps(sources, ensure_ascii=False)
            yield {"event": "sources", "data": sources_json}

            # Generate response using local service
            response_text = generate_local_response(message, context)

            # Stream the response in chunks
            words = response_text.split()
            for i, word in enumerate(words):
                if i == 0:
                    yield {"event": "chunk", "data": word}
                else:
                    yield {"event": "chunk", "data": f" {word}"}
        except Exception as fallback_error:
            print(f"Fallback also failed: {fallback_error}")
            yield {"event": "chunk", "data": f"Based on the book: I found information about this topic in the book, but I'm having trouble generating a full response. Please check if the book content covers this topic."}

        yield {"event": "done", "data": "true"}


def check_off_topic_query(message: str) -> Optional[str]:
    """
    Check if the query is off-topic and return an appropriate response if it is.
    Returns None if the query is on-topic.
    """
    # List of keywords that indicate off-topic queries
    off_topic_keywords = [
        'cook', 'food', 'recipe', 'pasta', 'pizza', 'weather', 'sports', 'movie', 'film',
        'music', 'celebrity', 'actor', 'actress', 'game', 'football', 'basketball', 'soccer',
        'stock', 'finance', 'money', 'investment', 'politics', 'election', 'president',
        'health', 'medical', 'doctor', 'medicine', 'treatment', 'disease', 'virus',
        'travel', 'vacation', 'hotel', 'restaurant', 'tourist', 'sightseeing',
        'car', 'automobile', 'driving', 'engine', 'mechanic', 'gasoline',
        'fashion', 'clothing', 'dress', 'shoes', 'designer', 'style',
        'education', 'school', 'university', 'student', 'teacher', 'classroom',
        'programming', 'software', 'computer', 'code', 'developer', 'python', 'javascript'
    ]

    message_lower = message.lower()

    # Check if any off-topic keywords are in the message
    for keyword in off_topic_keywords:
        if keyword in message_lower:
            return "I can only answer questions about the Physical AI & Humanoid Robotics textbook. Please ask questions related to the book content."

    # Additional check: if the query is very general and not related to robotics/AI
    general_keywords = ['hello', 'hi', 'how are you', 'what is your name', 'who are you', 'what can you do']
    if any(keyword in message_lower for keyword in general_keywords):
        return None  # Allow these as they might be just greetings

    # Check if the query contains book-related keywords
    book_related_keywords = [
        'humanoid', 'robot', 'robotics', 'ai', 'artificial intelligence', 'physical ai',
        'embodied', 'cognition', 'perception', 'locomotion', 'manipulation', 'control',
        'sensors', 'actuators', 'navigation', 'gait', 'balance', 'bipedal', 'locomotion',
        'human-robot', 'interaction', 'embodiment', 'grounded', 'cognition', 'sensory',
        'motor', 'behavior', 'learning', 'machine learning', 'neural', 'network'
    ]

    has_book_related = any(keyword in message_lower for keyword in book_related_keywords)

    # If it doesn't contain book-related keywords and seems like a specific non-book question
    if not has_book_related:
        # Additional check for common off-topic patterns
        off_topic_patterns = [
            'favorite', 'best', 'top', 'how to make', 'how to cook', 'recipe for',
            'weather in', 'what time is', 'where is', 'how far is', 'when was',
            'who invented', 'who discovered', 'who created'
        ]
        if any(pattern in message_lower for pattern in off_topic_patterns):
            return "I can only answer questions about the Physical AI & Humanoid Robotics textbook. Please ask questions related to the book content."

    return None


@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Return streaming response using SSE
    return EventSourceResponse(chat_stream(request.message, request.selected_text, request.current_page))