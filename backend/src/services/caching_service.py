from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from ..models.db_schema import TranslationCache, PersonalizationProfile
from datetime import datetime, timedelta
from uuid import UUID
import json


class CachingService:
    def __init__(self):
        pass
    
    async def cache_translation(
        self, 
        db: Session, 
        segment_id: UUID, 
        target_language: str, 
        translated_text: str
    ) -> bool:
        """
        Cache a translation in the database
        """
        try:
            # Check if a cache entry already exists for this segment and language
            existing_cache = db.query(TranslationCache).filter(
                TranslationCache.segment_id == segment_id,
                TranslationCache.target_language == target_language
            ).first()
            
            if existing_cache:
                # Update existing cache entry
                existing_cache.translated_text = translated_text
                existing_cache.created_at = datetime.utcnow()
            else:
                # Create new cache entry
                cache_entry = TranslationCache(
                    segment_id=segment_id,
                    target_language=target_language,
                    translated_text=translated_text
                )
                db.add(cache_entry)
            
            db.commit()
            return True
        except Exception as e:
            print(f"Error caching translation: {str(e)}")
            db.rollback()
            return False
    
    async def get_cached_translation(
        self, 
        db: Session, 
        segment_id: UUID, 
        target_language: str
    ) -> Optional[str]:
        """
        Retrieve a cached translation from the database
        """
        try:
            cache_entry = db.query(TranslationCache).filter(
                TranslationCache.segment_id == segment_id,
                TranslationCache.target_language == target_language
            ).first()
            
            if cache_entry:
                return cache_entry.translated_text
            return None
        except Exception as e:
            print(f"Error retrieving cached translation: {str(e)}")
            return None
    
    async def cache_personalized_content(
        self, 
        db: Session, 
        user_id: UUID, 
        chapter_id: str, 
        personalized_content: Dict[str, Any]
    ) -> bool:
        """
        Cache personalized content for a user and chapter
        """
        try:
            # Convert personalized content to JSON string for storage
            content_str = json.dumps(personalized_content)
            
            # Check if a profile already exists for this user
            profile = db.query(PersonalizationProfile).filter(
                PersonalizationProfile.user_id == user_id
            ).first()
            
            if profile:
                # Add the new personalized content to the existing profile's preferences
                if profile.preferences is None:
                    profile.preferences = {}
                
                # Create a key for this specific chapter's personalized content
                cache_key = f"personalized_content_{chapter_id}"
                profile.preferences[cache_key] = content_str
                profile.preferences[f"{cache_key}_timestamp"] = datetime.utcnow().isoformat()
            else:
                # Create a new profile with the personalized content
                profile = PersonalizationProfile(
                    user_id=user_id,
                    preferences={
                        f"personalized_content_{chapter_id}": content_str,
                        f"personalized_content_{chapter_id}_timestamp": datetime.utcnow().isoformat()
                    }
                )
                db.add(profile)
            
            db.commit()
            return True
        except Exception as e:
            print(f"Error caching personalized content: {str(e)}")
            db.rollback()
            return False
    
    async def get_cached_personalized_content(
        self, 
        db: Session, 
        user_id: UUID, 
        chapter_id: str,
        cache_duration_hours: int = 24  # Default to 24-hour cache
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached personalized content for a user and chapter
        """
        try:
            profile = db.query(PersonalizationProfile).filter(
                PersonalizationProfile.user_id == user_id
            ).first()
            
            if profile and profile.preferences:
                # Create a key for this specific chapter's personalized content
                cache_key = f"personalized_content_{chapter_id}"
                timestamp_key = f"{cache_key}_timestamp"
                
                # Check if the content exists and if it's still within the cache duration
                if cache_key in profile.preferences and timestamp_key in profile.preferences:
                    content_str = profile.preferences[cache_key]
                    timestamp_str = profile.preferences[timestamp_key]
                    
                    # Parse the timestamp and check if it's still valid
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    if datetime.utcnow() - timestamp < timedelta(hours=cache_duration_hours):
                        # Content is still valid, return it
                        return json.loads(content_str)
            
            # No valid cached content found
            return None
        except Exception as e:
            print(f"Error retrieving cached personalized content: {str(e)}")
            return None
    
    async def invalidate_translation_cache(
        self, 
        db: Session, 
        segment_id: UUID = None, 
        target_language: str = None
    ) -> bool:
        """
        Invalidate specific translation cache entries
        """
        try:
            query = db.query(TranslationCache)
            
            if segment_id:
                query = query.filter(TranslationCache.segment_id == segment_id)
            if target_language:
                query = query.filter(TranslationCache.target_language == target_language)
            
            query.delete()
            db.commit()
            return True
        except Exception as e:
            print(f"Error invalidating translation cache: {str(e)}")
            db.rollback()
            return False
    
    async def invalidate_personalization_cache(
        self, 
        db: Session, 
        user_id: UUID = None, 
        chapter_id: str = None
    ) -> bool:
        """
        Invalidate specific personalization cache entries
        """
        try:
            if user_id and chapter_id:
                # Only invalidate specific user's cache for a chapter
                profile = db.query(PersonalizationProfile).filter(
                    PersonalizationProfile.user_id == user_id
                ).first()
                
                if profile and profile.preferences:
                    cache_key = f"personalized_content_{chapter_id}"
                    timestamp_key = f"{cache_key}_timestamp"
                    
                    # Remove the specific cached content
                    profile.preferences.pop(cache_key, None)
                    profile.preferences.pop(timestamp_key, None)
                    
                    db.commit()
            elif user_id:
                # Invalidate all of a user's personalization cache
                profile = db.query(PersonalizationProfile).filter(
                    PersonalizationProfile.user_id == user_id
                ).first()
                
                if profile and profile.preferences:
                    # Remove all personalization cache entries
                    new_preferences = {}
                    for key, value in profile.preferences.items():
                        if not key.startswith("personalized_content_"):
                            new_preferences[key] = value
                    
                    profile.preferences = new_preferences
                    db.commit()
            
            return True
        except Exception as e:
            print(f"Error invalidating personalization cache: {str(e)}")
            db.rollback()
            return False