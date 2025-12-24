from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import asyncio
import logging
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the RAG system components

app = FastAPI(
    title="Book RAG Chatbot API for Hugging Face Space",
    description="API for querying book content using RAG with /api/ask endpoint",
    version="0.1.0"
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class AskResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    return {"message": "Book RAG Chatbot Backend API", "status": "running"}

@app.get("/health")
async def health_check():
    # Import RAG system components inside the function to avoid initialization issues
    from src.rag_chatbot.main import rag_chatbot_system
    # Perform health check
    health_status = await rag_chatbot_system.health_check()
    return health_status

@app.post("/api/ask")
async def ask_endpoint(ask_request: AskRequest):
    """
    Endpoint that matches the frontend expectation at /api/ask
    """
    try:
        logger.info(f"Received query: {ask_request.query[:50]}...")

        # Import RAG system components inside the function to avoid initialization issues
        from src.rag_chatbot.main import rag_chatbot_system
        from src.rag_chatbot.models.query_models import QueryRequest

        # Create a QueryRequest object from the input
        query_request = QueryRequest(
            query=ask_request.query,
            user_id=ask_request.user_id,
            session_id=ask_request.session_id,
            context_window=5,
            include_citations=True
        )

        # Process the query using the rag chatbot system
        response = await rag_chatbot_system.process_query(query_request)

        # Return only the response text as expected by the frontend
        return {"response": response.response}

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_endpoint(ask_request: AskRequest):
    """
    Endpoint that matches the updated frontend expectation at /chat
    """
    try:
        logger.info(f"Received chat query: {ask_request.query[:50]}...")

        # Import RAG system components inside the function to avoid initialization issues
        from src.rag_chatbot.main import rag_chatbot_system
        from src.rag_chatbot.models.query_models import QueryRequest

        # Create a QueryRequest object from the input
        query_request = QueryRequest(
            query=ask_request.query,
            user_id=ask_request.user_id,
            session_id=ask_request.session_id,
            context_window=5,
            include_citations=True
        )

        # Process the query using the rag chatbot system
        response = await rag_chatbot_system.process_query(query_request)

        # Return only the response text as expected by the frontend
        return {"response": response.response}

    except Exception as e:
        logger.error(f"Error processing chat query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Alternative endpoint in case we need to support GET requests too
@app.get("/api/ask")
async def ask_endpoint_get(query: str):
    """
    GET version of the ask endpoint for compatibility
    """
    try:
        logger.info(f"Received GET query: {query[:50]}...")

        # Import RAG system components inside the function to avoid initialization issues
        from src.rag_chatbot.main import rag_chatbot_system
        from src.rag_chatbot.models.query_models import QueryRequest

        # Create a QueryRequest object from the input
        query_request = QueryRequest(
            query=query,
            context_window=5,
            include_citations=True
        )

        # Process the query using the rag chatbot system
        response = await rag_chatbot_system.process_query(query_request)

        # Return only the response text as expected by the frontend
        return {"response": response.response}

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat")
async def chat_endpoint_get(query: str):
    """
    GET version of the chat endpoint for compatibility
    """
    try:
        logger.info(f"Received GET chat query: {query[:50]}...")

        # Import RAG system components inside the function to avoid initialization issues
        from src.rag_chatbot.main import rag_chatbot_system
        from src.rag_chatbot.models.query_models import QueryRequest

        # Create a QueryRequest object from the input
        query_request = QueryRequest(
            query=query,
            context_window=5,
            include_citations=True
        )

        # Process the query using the rag chatbot system
        response = await rag_chatbot_system.process_query(query_request)

        # Return only the response text as expected by the frontend
        return {"response": response.response}

    except Exception as e:
        logger.error(f"Error processing chat query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))