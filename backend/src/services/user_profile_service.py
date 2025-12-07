from typing import Optional
from sqlalchemy.orm import Session
from ..models.db_schema import User as UserDBModel, PersonalizationProfile as ProfileDBModel
from ..models.user import UserInDB, UserUpdate
from uuid import UUID


class UserProfileService:
    def __init__(self):
        pass
    
    async def get_user_profile(self, db: Session, user_id: UUID) -> Optional[UserInDB]:
        """
        Retrieve a user's profile information
        """
        db_user = db.query(UserDBModel).filter(UserDBModel.user_id == user_id).first()
        if db_user is None:
            return None
        
        return UserInDB(
            user_id=db_user.user_id,
            email=db_user.email,
            background_info=db_user.background_info,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
    
    async def update_user_profile(self, db: Session, user_id: UUID, profile_update: UserUpdate) -> Optional[UserInDB]:
        """
        Update a user's profile information
        """
        db_user = db.query(UserDBModel).filter(UserDBModel.user_id == user_id).first()
        if db_user is None:
            return None
        
        # Update the fields that are provided
        if profile_update.background_info is not None:
            db_user.background_info = profile_update.background_info
        
        if profile_update.personalization_preferences is not None:
            # If personalization preferences exist, update or create the profile
            profile = db.query(ProfileDBModel).filter(ProfileDBModel.user_id == user_id).first()
            if profile:
                profile.preferences = profile_update.personalization_preferences
            else:
                profile = ProfileDBModel(
                    user_id=user_id,
                    preferences=profile_update.personalization_preferences
                )
                db.add(profile)
        
        db.commit()
        db.refresh(db_user)
        
        return UserInDB(
            user_id=db_user.user_id,
            email=db_user.email,
            background_info=db_user.background_info,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
    
    async def create_personalization_profile(self, db: Session, user_id: UUID, preferences: dict) -> Optional[ProfileDBModel]:
        """
        Create or update a user's personalization profile
        """
        profile = db.query(ProfileDBModel).filter(ProfileDBModel.user_id == user_id).first()
        
        if profile:
            profile.preferences = preferences
        else:
            profile = ProfileDBModel(
                user_id=user_id,
                preferences=preferences
            )
            db.add(profile)
        
        db.commit()
        db.refresh(profile)
        return profile
    
    async def get_personalization_profile(self, db: Session, user_id: UUID) -> Optional[ProfileDBModel]:
        """
        Retrieve a user's personalization profile
        """
        profile = db.query(ProfileDBModel).filter(ProfileDBModel.user_id == user_id).first()
        return profile