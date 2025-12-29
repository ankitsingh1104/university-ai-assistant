"""
Embedding generation using SentenceTransformers
Converts text documents and queries to semantic embeddings for similarity search
"""

from sentence_transformers import SentenceTransformer
import numpy as np
import logging
from typing import List

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """
    Generate embeddings for documents and queries using SentenceTransformers
    Uses lightweight models for efficient local inference
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding model
        
        Args:
            model_name: HuggingFace model ID (lightweight model for efficiency)
        
        Models available:
        - all-MiniLM-L6-v2: Fast, 384 dimensions (default)
        - all-mpnet-base-v2: Accurate, 768 dimensions
        - paraphrase-MiniLM-L6-v2: Paraphrase detection
        """
        try:
            self.model = SentenceTransformer(model_name)
            self.embedding_dim = self.model.get_sentence_embedding_dimension()
            logger.info(f"✅ Loaded embedding model: {model_name} ({self.embedding_dim}D)")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise
    
    def embed(self, texts: List[str]) -> np.ndarray:
        """
        Embed a list of texts to semantic vectors
        
        Args:
            texts: List of text strings to embed
        
        Returns:
            numpy array of shape (len(texts), embedding_dim)
        
        Example:
            >>> embeddings = generator.embed(["Hello world", "Hi there"])
            >>> embeddings.shape
            (2, 384)
        """
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            logger.debug(f"Embedded {len(texts)} texts to {embeddings.shape}")
            return embeddings
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            raise
