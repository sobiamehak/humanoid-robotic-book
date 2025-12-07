from typing import Optional
from ..models.user import UserCreate, UserInDB
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..models.db_schema import User as UserDBModel
from uuid import UUID
import uuid

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        pass

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password
        """
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Generate a hash for a plain password
        """
        return pwd_context.hash(password)

    async def create_user(self, db: Session, user_data: UserCreate) -> UserInDB:
        """
        Create a new user in the database
        """
        # Hash the password
        hashed_password = self.get_password_hash(user_data.password)

        # Create the database user object
        db_user = UserDBModel(
            email=user_data.email,
            password_hash=hashed_password,
            background_info=user_data.background_info
        )

        # Add to database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Convert to Pydantic model and return
        return UserInDB(
            user_id=db_user.user_id,
            email=db_user.email,
            background_info=db_user.background_info,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )

    async def get_user_by_email(self, db: Session, email: str) -> Optional[UserInDB]:
        """
        Retrieve a user by email
        """
        db_user = db.query(UserDBModel).filter(UserDBModel.email == email).first()
        if db_user is None:
            return None

        return UserInDB(
            user_id=db_user.user_id,
            email=db_user.email,
            background_info=db_user.background_info,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )

    async def authenticate_user(self, db: Session, email: str, password: str) -> Optional[UserInDB]:
        """
        Authenticate a user by email and password
        """
        user = await self.get_user_by_email(db, email)
        if not user:
            return None

        # In a real implementation, we would need to hash the password and compare
        # For this example, I'll just verify against the database
        db_user = db.query(UserDBModel).filter(UserDBModel.email == email).first()
        if not db_user or not self.verify_password(password, db_user.password_hash):
            return None

        return user