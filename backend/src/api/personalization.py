from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from ..services.personalization_service import PersonalizationService
from ..services.user_profile_service import UserProfileService
from ..config import get_db

router = APIRouter(prefix="/personalization", tags=["personalization"])

class PersonalizeRequest(BaseModel):
    chapter_id: str
    content: str
    user_id: Optional[UUID] = None

class PersonalizeResponse(BaseModel):
    original_content: str
    personalized_content: str
    personalization_notes: list
    confidence_score: float

@router.post("/personalize", response_model=PersonalizeResponse)
async def personalize_content(
    request: PersonalizeRequest,
    db: Session = Depends(get_db)
):
    """
    Request personalized content for a chapter based on user profile
    """
    try:
        personalization_service = PersonalizationService()
        user_profile_service = UserProfileService()
        
        # Get user profile if user_id is provided
        user_background = {}
        if request.user_id:
            user_profile = await user_profile_service.get_user_profile(db, request.user_id)
            if user_profile and user_profile.background_info:
                user_background = user_profile.background_info
            else:
                # If no profile exists, use defaults
                user_background = {
                    "academicLevel": "graduate",
                    "areasOfInterest": "general",
                    "learningStyle": "reading"
                }
        
        # Personalize the content
        result = await personalization_service.personalize_content_with_json(
            request.content,
            user_background
        )
        
        return PersonalizeResponse(
            original_content=result["original_content"],
            personalized_content=result["personalized_content"],
            personalization_notes=result["personalization_notes"],
            confidence_score=result["confidence_score"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing personalization request: {str(e)}"
        )