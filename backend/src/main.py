from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import config
from .models import db_schema
from .api import chatbot, auth, personalization, translation

app = FastAPI(
    title="Physical AI & Humanoid Robotics Textbook API",
    version="1.0.0",
    description="API for managing textbook content, user authentication, RAG chatbot, personalization, and translation features."
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
db_schema.Base.metadata.create_all(bind=config.engine)

# Include API routes
app.include_router(chatbot.router)
app.include_router(auth.router)
app.include_router(personalization.router)
app.include_router(translation.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "FastAPI is running!"}

@app.on_event("startup")
def startup_event():
    """
    Initialize the RAG system when the server starts.
    This will load all textbook content into the vector database.
    """
    print("Initializing RAG system...")
    try:
        from .init_rag_system import initialize_rag_system
        success = initialize_rag_system()
        if success:
            print("RAG system initialized successfully!")
        else:
            print("Warning: RAG system initialization failed!")
    except Exception as e:
        print(f"Error initializing RAG system: {str(e)}")

# Dependency to get the database session
def get_db():
    db = config.SessionLocal()
    try:
        yield db
    finally:
        db.close()
