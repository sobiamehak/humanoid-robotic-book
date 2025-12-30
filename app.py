"""
Hugging Face Space API Entry Point for RAG Chatbot Backend
This file serves as the entry point for the Hugging Face Space deployment.
"""
import sys
import os
from pathlib import Path

# Add the api/src directory to the Python path so we can import from it
api_path = Path(__file__).parent / "api" / "src"
sys.path.insert(0, str(api_path))

# Import the FastAPI app from the API backend
from main import app as api_app
from config.settings import settings

# Override settings for Hugging Face environment if needed
if os.getenv("HF_SPACE_ID"):
    # Hugging Face specific configurations
    print(f"Running in Hugging Face Space: {os.getenv('HF_SPACE_ID')}")

# The app instance that Hugging Face will use
app = api_app

# This is the entry point for Hugging Face Spaces
# The space will look for a 'app' variable that is a FastAPI instance