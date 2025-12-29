"""Semantic search service."""
import os
from typing import List, Dict, Any
import openai
from backend.services.rag_service import RAGService

class SemanticSearchService:
    """Semantic search service using vector embeddings."""
    
    def __init__(self):
        """Initialize semantic search service."""
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.rag_service = RAGService()
        self.top_k = int(os.getenv('TOP_K_RESULTS', 5))
    
    def search(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """Perform semantic search on indexed documents."""
        if top_k is None:
            top_k = self.top_k
        
        results = self.rag_service.retrieve(query, top_k=top_k)
        
        formatted_results = []
        for result in results:
            formatted_results.append({
                'id': result.get('id'),
                'score': result.get('score'),
                'text': result.get('metadata', {}).get('text', ''),
                'doc_id': result.get('metadata', {}).get('doc_id', '')
            })
        
        return formatted_results
    
    def search_with_filters(self, query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Perform semantic search with filters."""
        results = self.rag_service.retrieve(query, top_k=self.top_k)
        
        if filters:
            results = self._apply_filters(results, filters)
        
        return results
    
    def _apply_filters(self, results: List[Dict], filters: Dict[str, Any]) -> List[Dict]:
        """Apply filters to search results."""
        filtered = []
        for result in results:
            metadata = result.get('metadata', {})
            if all(metadata.get(k) == v for k, v in filters.items()):
                filtered.append(result)
        return filtered
