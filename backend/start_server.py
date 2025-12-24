#!/usr/bin/env python3
"""
Start script for the Physical AI & Humanoid Robotics Textbook API
This will start the FastAPI server with the RAG chatbot functionality
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Get host and port from environment variables or use defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    print(f"Starting server on {host}:{port}")
    print("Loading textbook content into RAG system (this may take a moment)...")
    
    # Start the Uvicorn server
    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )

if __name__ == "__main__":
    main()