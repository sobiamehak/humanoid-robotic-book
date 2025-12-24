from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

# Pydantic models for API serialization/validation
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    background_info: Optional[Dict[str, Any]] = None

class UserUpdate(BaseModel):
    background_info: Optional[Dict[str, Any]] = None
    personalization_preferences: Optional[Dict[str, Any]] = None

class UserInDB(UserBase):
    user_id: UUID
    background_info: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True