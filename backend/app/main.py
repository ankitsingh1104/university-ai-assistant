"""
University AI Assistant - FastAPI Backend
Main application entry point for chat and semantic search

Architecture:
- FastAPI REST API
- FAISS vector store for embeddings
- SentenceTransformers for semantic search
- Local LLM inference (no cloud dependencies)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
from pathlib import Path
import os

from app.api import chat, search
from app.core.vector_store import VectorStore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="University AI Assistant",
    description="AI-powered semantic search and chat for university information",
    version="1.0.0"
)

# CORS configuration - allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize vector store on startup
@app.on_event("startup")
async def startup_event():
    """Initialize vector store and load embeddings"""
    try:
        logger.info("Initializing vector store...")
        vector_store = VectorStore()
        vector_store.load_documents()
        logger.info("✅ Vector store initialized successfully")
        app.state.vector_store = vector_store
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {e}")
        raise

# Mount static files for frontend
static_path = Path(__file__).parent.parent.parent / "frontend"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Include API routers
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(search.router, prefix="/api", tags=["search"])

@app.get("/")
async def root():
    """Root endpoint - returns API info"""
    return {
        "name": "University AI Assistant",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )
