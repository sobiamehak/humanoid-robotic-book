import asyncio
import os
from dotenv import load_dotenv

from agents import Agent, RunConfig, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from openai import AsyncOpenAI
from qdrant_client import QdrantClient
import cohere

# 🚫 Disable tracing
set_tracing_disabled(disabled=True)

# 🔐 Load environment variables
load_dotenv()

# Qdrant Configuration
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "book-rag-db")

# Cohere for embeddings (same model used when indexing)
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize clients
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
cohere_client = cohere.AsyncClient(COHERE_API_KEY)

# 🌐 OpenRouter client (OpenAI-compatible)
external_client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# 🧠 Choose a good model on OpenRouter (free/fast: meta-llama/llama-3.1-8b-instruct or anthropic/claude-3-haiku)
MODEL_NAME = "anthropic/claude-3.5-sonnet"  # Strong reasoning, good for RAG

model = OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client=external_client
)

# ⚙️ Run configuration
config = RunConfig(
    model=model,
    model_provider=external_client,  # Ensures consistent model across handoffs
    tracing_disabled=True
)

# 🔧 Retrieval Tool using Cohere embeddings + Qdrant search
@function_tool
async def retrieve_book_context(query: str) -> str:
    """
    Retrieve relevant chunks from the book about physical AI humanoid robotics.
    Use this tool whenever the user asks a question related to the book content.
    """
    # Embed the query using Cohere
    embed_response = await cohere_client.embed(
        texts=[query],
        model="embed-english-v3.0",  # Use the same model as when you indexed
        input_type="search_query"
    )
    query_embedding = embed_response.embeddings[0]

    # Search in Qdrant
    search_results = qdrant_client.search(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=query_embedding,
        limit=5,  # top_k=5
        score_threshold=0.0  # No threshold, get all relevant
    )

    if not search_results:
        return "No relevant information found in the book."

    # Format retrieved chunks
    contexts = []
    for i, hit in enumerate(search_results, 1):
        text = hit.payload.get("text", "No text")
        chapter = hit.payload.get("chapter", "Unknown chapter")
        contexts.append(f"[Chunk {i} - Chapter: {chapter}]\n{text}\n")

    return "\n".join(contexts)

# 🤖 Generation Agent: Uses retrieved context to answer accurately
generation_agent = Agent(
    name="Book Answer Agent",
    instructions="""
You are an expert on the book about Physical AI Humanoid Robotics (12 chapters).
Answer user questions ONLY using the provided retrieved context from the book.
- Be accurate, detailed, and cite the relevant chapters or sections.
- Quote important parts directly from the context.
- If the context does not contain enough information, say: "I don't have sufficient information from the book to answer this fully."
- Never make up information not present in the context.
- Keep responses clear, structured, and helpful.
""",
    model=model
)

# 🧠 Main Orchestrator Agent: Decides to retrieve then generate
main_agent = Agent(
    name="RAG Orchestrator",
    instructions="""
You are a helpful chatbot for questions about the book on Physical AI Humanoid Robotics.
- For any question related to the book's content, always use the 'retrieve_book_context' tool first to get relevant chunks.
- After retrieval, hand off to the Book Answer Agent to generate the final response.
- If the question is general greeting or off-topic (not about the book), respond politely and briefly.
- Stay focused on the book topic.
""",
    tools=[retrieve_book_context],
    handoffs=[generation_agent],
    model=model
)

# 🚀 Async main function with conversation loop
async def main():
    print("🤖 Book RAG Chatbot Ready! Ask about Physical AI Humanoid Robotics (type 'exit' to quit)\n")
    
    while True:
        user_message = input("You: ").strip()
        if user_message.lower() in ["exit", "quit", "bye"]:
            print("Goodbye! 👋")
            break
        if not user_message:
            continue

        print("Thinking...\n")
        result = await Runner.run(main_agent, user_message, run_config=config)
        print("Bot:", result.final_output, "\n")

# 🔄 Run the chatbot
if __name__ == "__main__":
    asyncio.run(main())