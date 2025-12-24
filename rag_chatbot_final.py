import asyncio
import os
import re
from dotenv import load_dotenv

from agents import Agent, RunConfig, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from openai import AsyncOpenAI
from qdrant_client import QdrantClient
import cohere

set_tracing_disabled(disabled=True)

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "book-rag-db")

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
cohere_client = cohere.AsyncClient(COHERE_API_KEY)

external_client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

MODEL_NAME = "anthropic/claude-3.5-sonnet"

model = OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

def is_greeting_or_off_topic(query: str) -> bool:
    """
    Determine if the query is a greeting or off-topic message that doesn't require RAG retrieval.
    """
    query_lower = query.lower().strip()

    # Common greetings and simple off-topic phrases
    greetings = [
        'hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'good night',
        'howdy', 'what\'s up', 'sup', 'yo', 'morning', 'afternoon', 'evening'
    ]

    # Simple affirmations/negations that are likely off-topic
    simple_responses = [
        'yes', 'no', 'maybe', 'ok', 'okay', 'sure', 'thanks', 'thank you', 'please',
        'please help', 'help', 'can you help', 'assist me'
    ]

    # Check for greetings
    if query_lower in greetings:
        return True

    # Check for simple responses
    if query_lower in simple_responses:
        return True

    # Check for greeting-like patterns (e.g., "hi there", "hello there")
    greeting_patterns = [
        r'^(hi|hello|hey|greetings)\s*(there|there!|!)?$',
        r'^good\s+(morning|afternoon|evening|night)',
        r'^(what\'s|whats)\s+up',
        r'^how\s+are\s+you',
        r'^howdy',
        r'^what\'?s\s+new',
        r'^long\s+time\s+no\s+see',
        r'^nice\s+to\s+meet\s+you',
        r'^pleased\s+to\s+meet\s+you',
        r'^how\s+do\s+you\s+do',
        r'^good\s+to\s+see\s+you'
    ]

    for pattern in greeting_patterns:
        if re.match(pattern, query_lower):
            return True

    # Check if query is very short and doesn't contain question words or book-related terms
    if len(query.split()) <= 2 and not any(word in query_lower for word in [
        'what', 'how', 'why', 'when', 'where', 'who', 'which', 'explain', 'describe',
        'chapter', 'robot', 'ai', 'humanoid', 'physical', 'book', 'topic', 'section'
    ]):
        return True

    return False

@function_tool
async def retrieve_book_context(query: str) -> str:
    """
    Retrieve relevant book context from Qdrant based on the query.
    """
    embed_response = await cohere_client.embed(
        texts=[query],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    query_embedding = embed_response.embeddings[0]

    search_results = qdrant_client.search(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=query_embedding,
        limit=5,
        score_threshold=0.0
    )

    if not search_results:
        return "No relevant information found in the book."

    contexts = []
    for i, hit in enumerate(search_results, 1):
        text = hit.payload.get("text", "No text")
        chapter = hit.payload.get("chapter", "Unknown chapter")
        contexts.append(f"[Chunk {i} - Chapter: {chapter}]\n{text}\n")

    return "\n".join(contexts)

@function_tool
async def smart_respond(query: str) -> str:
    """
    Smart response function that handles both greetings/off-topic and book questions appropriately.
    """
    if is_greeting_or_off_topic(query):
        # For greetings or off-topic, return a simple response without RAG
        query_lower = query.lower().strip()
        if query_lower in ['hi', 'hello', 'hey', 'greetings']:
            return "Hello! Ask about the book on Physical AI Humanoid Robotics."
        elif query_lower in ['yes', 'no', 'maybe', 'ok', 'okay', 'sure', 'thanks', 'thank you']:
            return "Got it! Feel free to ask questions about the book on Physical AI Humanoid Robotics."
        elif query_lower in ['good morning', 'good afternoon', 'good evening', 'good night']:
            return f"{query.capitalize()}! Feel free to ask questions about the book on Physical AI Humanoid Robotics."
        else:
            return "Hello! Feel free to ask questions about the book on Physical AI Humanoid Robotics."
    else:
        # For book questions, retrieve context and return it for the agent to process
        context = await retrieve_book_context(query)
        return f"RETRIEVED_CONTEXT:\n{context}"

# Main agent that intelligently handles both greetings and book questions
main_agent = Agent(
    name="Smart RAG Chatbot",
    instructions="Use the smart_respond tool to handle user queries. "
                "For greetings and off-topic queries (like 'hi', 'hello', 'yes', 'no', 'thanks'), "
                "respond with simple, friendly messages inviting questions about the book. "
                "For actual book questions, retrieve relevant context using RAG and provide "
                "accurate answers citing chapters from the book. "
                "Always respond concisely, stick to the book content, and avoid hallucinations. "
                "When RETRIEVED_CONTEXT is provided, use it to answer the question accurately.",
    tools=[smart_respond, retrieve_book_context],
    model=model
)

async def main():
    print("Book RAG Chatbot Ready! Ask about the book (type 'exit' to quit)\n")
    while True:
        user_message = input("You: ").strip()
        if user_message.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        if not user_message:
            continue
        print("Thinking...\n")
        result = await Runner.run(main_agent, user_message, run_config=config)
        print("Bot:", result.final_output, "\n")

if __name__ == "__main__":
    asyncio.run(main())