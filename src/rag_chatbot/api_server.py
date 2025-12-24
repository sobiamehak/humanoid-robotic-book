from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import asyncio
import logging
from src.rag_chatbot.main import rag_chatbot_system
from src.rag_chatbot.models.query_models import QueryRequest

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Book RAG Chatbot API",
    description="API for querying book content using RAG",
    version="0.1.0"
)

class QueryInput(BaseModel):
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    context_window: Optional[int] = 5
    include_citations: Optional[bool] = True

class QueryOutput(BaseModel):
    response: str
    query_id: str
    citations: Optional[list] = []
    context_used: Optional[list] = []
    is_off_topic: Optional[bool] = False

@app.get("/")
def read_root():
    return {"message": "Book RAG Chatbot Backend API", "status": "running"}

@app.get("/health")
async def health_check():
    # Perform health check
    health_status = await rag_chatbot_system.health_check()
    return health_status

@app.post("/query", response_model=QueryOutput)
async def process_query(query_input: QueryInput):
    try:
        # Create a QueryRequest object from the input
        query_request = QueryRequest(
            query=query_input.query,
            user_id=query_input.user_id,
            session_id=query_input.session_id,
            context_window=query_input.context_window,
            include_citations=query_input.include_citations
        )

        # Process the query using the rag chatbot system
        response = await rag_chatbot_system.process_query(query_request)

        return response
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)