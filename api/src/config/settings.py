from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    gemini_api_key: str = "AIzaSyAjDfTQv98Bk8aLWBgvKH2lWAsdlfNPE24"
    openrouter_api_key: str = ""
    openrouter_model: str = "google/gemini-pro"  # Default model
    qdrant_url: str = "https://1d09eb51-1927-4f41-9f2e-a22ff508dfb3.us-east4-0.gcp.cloud.qdrant.io:6333"
    qdrant_api_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.f2nAgzLS7D7X1ULiqXq5JrlS89OPq1gmxWWNp7WO3AI"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()