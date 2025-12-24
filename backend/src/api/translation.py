from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from ..services.translation_service import TranslationService
from ..config import get_db

router = APIRouter(prefix="/translation", tags=["translation"])

class TranslateRequest(BaseModel):
    chapter_id: str
    content: str
    segment_id: Optional[UUID] = None
    user_id: Optional[UUID] = None

class TranslateResponse(BaseModel):
    original_content: str
    translated_content: str

@router.get("/{chapter_id}/urdu", response_model=TranslateResponse)
async def get_urdu_translation(
    chapter_id: str,
    db: Session = Depends(get_db)
):
    """
    Get Urdu translation of a chapter's content
    """
    # This endpoint would typically get the content from the database
    # For now, this is a placeholder implementation
    raise HTTPException(status_code=501, detail="Endpoint not implemented yet - requires content retrieval logic")

@router.post("/urdu", response_model=TranslateResponse)
async def translate_to_urdu(
    request: TranslateRequest,
    db: Session = Depends(get_db)
):
    """
    Request Urdu translation of content
    """
    try:
        translation_service = TranslationService()
        
        # Perform the Urdu translation
        translated_content = await translation_service.translate_chapter_content(
            request.content,
            db,
            request.chapter_id,
            request.segment_id
        )
        
        return TranslateResponse(
            original_content=request.content,
            translated_content=translated_content
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing translation request: {str(e)}"
        )