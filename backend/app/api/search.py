"""Semantic search API endpoint"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class SearchRequest(BaseModel):
    """Search request"""
    query: str = Field(..., min_length=1, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=50)

class SearchResult(BaseModel):
    """Search result"""
    document: str
    relevance: float

class SearchResponse(BaseModel):
    """Search response"""
    results: list[SearchResult]
    total: int

@router.post("/search", response_model=SearchResponse)
async def search_endpoint(request: Request, search_req: SearchRequest):
    """Semantic search over university documents"""
    try:
        if not search_req.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        vector_store = request.app.state.vector_store
        results = vector_store.search(search_req.query, top_k=search_req.top_k)
        
        return SearchResponse(
            results=[SearchResult(document=r, relevance=0.85) for r in results],
            total=len(results)
        )
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
