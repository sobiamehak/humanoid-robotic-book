"""
Hugging Face Space entry point for the Book RAG Chatbot
This file serves as the entry point for the Hugging Face Space deployment.
"""
from api_server import app

# This is the entry point for Hugging Face Spaces
# The space will look for a 'app' variable that is a FastAPI instance