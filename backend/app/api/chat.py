"""
Chat API endpoint for conversational Q&A with RAG
Handles user queries and returns AI-generated responses with source citations
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    """Chat request model"""
    query: str = Field(..., min_length=1, max_length=1000)
    max_tokens: int = Field(default=512, ge=50, le=2048)

class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    sources: list = Field(default_factory=list)

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: Request, chat_req: ChatRequest):
    """
    Chat endpoint - conversational Q&A with RAG
    
    Retrieves relevant documents and generates response using local LLM
    
    Args:
        request: FastAPI request object
        chat_req: ChatRequest object with user query
    
    Returns:
        ChatResponse with generated answer and sources
    
    Raises:
        HTTPException: If query is invalid or processing fails
    """
    try:
        if not chat_req.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Get vector store from app state
        vector_store = request.app.state.vector_store
        
        # Search for relevant documents
        results = vector_store.search(chat_req.query, top_k=3)
        
        # Format context from search results
        context = "\n".join([f"- {doc[:100]}" for doc in results])
        
        # Generate response using mock LLM
        response = generate_response(chat_req.query, context)
        
        logger.info(f"Chat query processed: {chat_req.query[:50]}...")
        
        return ChatResponse(
            response=response,
            sources=results
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process chat query")

def generate_response(query: str, context: str) -> str:
    """
    Generate response using retrieved context
    In production, this would use an actual LLM like Mistral or LLaMA
    
    Args:
        query: User query
        context: Retrieved context from vector search
    
    Returns:
        Generated response string
    """
    # Mock implementation - replace with actual LLM inference
    if not context.strip():
        return f"I couldn't find specific information about '{query}'. Please try a different question."
    
    return f"Based on our university information: {context[:200]}... For more details, please check the sources provided."
