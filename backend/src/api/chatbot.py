from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from uuid import UUID
from ..services.rag_service import RAGService  # Use the original RAG service
from ..services.user_profile_service import UserProfileService
from ..config import get_db

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

class ChatQueryRequest(BaseModel):
    query: str
    context_type: str = "entire_book"  # "entire_book" or "selected_text"
    selected_text: Optional[str] = None
    user_id: Optional[UUID] = None

class SourceCitation(BaseModel):
    chapter_id: str
    module_id: str
    title: str
    score: float
    content_snippet: str

class ChatResponse(BaseModel):
    query: str
    response: str
    sources: List[SourceCitation]

@router.post("/query", response_model=ChatResponse)
async def query_chatbot(
    request: ChatQueryRequest,
    db: Session = Depends(get_db)
):
    """
    Query the RAG chatbot for answers from the textbook
    """
    try:
        rag_service = RAGService()
        user_profile_service = UserProfileService()

        # If user_id is provided, get their profile for personalization context
        user_context = None
        if request.user_id:
            user_profile = await user_profile_service.get_user_profile(db, request.user_id)
            if user_profile:
                user_context = {
                    "background_info": user_profile.background_info
                }

        # Query the RAG service with selected text and context type
        result = rag_service.query(
            query=request.query,
            user_id=request.user_id,
            user_context=user_context,
            selected_text=request.selected_text,
            context_type=request.context_type
        )

        return ChatResponse(
            query=result["query"],
            response=result["response"],
            sources=result["sources"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chatbot query: {str(e)}")