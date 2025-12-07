from sqlalchemy import Column, String, JSON, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import func
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    background_info = Column(JSON, default=dict)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    personalization_profiles = relationship("PersonalizationProfile", back_populates="user")
    chatbot_interactions = relationship("ChatbotInteraction", back_populates="user")

class ChapterContentSegment(Base):
    __tablename__ = "chapter_content_segments"

    segment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(String, index=True, nullable=False)
    module = Column(String, nullable=True)
    title = Column(String, nullable=True)
    content_text = Column(Text, nullable=False)
    vector_embedding = Column(JSON, nullable=True) # Stored as JSON for now, Qdrant will handle actual vectors
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    translations = relationship("TranslationCache", back_populates="content_segment")

class ChatbotInteraction(Base):
    __tablename__ = "chatbot_interactions"

    interaction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    query_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    source_citations = Column(JSON, default=list)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="chatbot_interactions")

class TranslationCache(Base):
    __tablename__ = "translation_cache"

    cache_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    segment_id = Column(UUID(as_uuid=True), ForeignKey("chapter_content_segments.segment_id"), nullable=False)
    target_language = Column(String, nullable=False)
    translated_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())

    content_segment = relationship("ChapterContentSegment", back_populates="translations")

class PersonalizationProfile(Base):
    __tablename__ = "personalization_profiles"

    profile_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    preferences = Column(JSON, default=dict)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="personalization_profiles")
