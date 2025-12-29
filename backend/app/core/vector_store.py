"""
Vector store using FAISS for semantic search and retrieval
Manages document embeddings and similarity search
"""

import faiss
import numpy as np
from pathlib import Path
import logging
from typing import List
from app.core.embeddings import EmbeddingGenerator

logger = logging.getLogger(__name__)

class VectorStore:
    """
    FAISS-based vector store for efficient semantic document retrieval
    Stores embeddings and provides fast nearest-neighbor search
    """
    
    def __init__(self, index_path: str = "data/vector_index.faiss"):
        """Initialize vector store"""
        self.index_path = index_path
        self.embedding_gen = EmbeddingGenerator()
        self.documents: List[str] = []
        self.index = None
        logger.info("VectorStore initialized")
    
    def load_documents(self):
        """Load documents from files and build FAISS index"""
        data_dir = Path("data/sample_documents")
        
        # Create sample documents if they don't exist
        if not data_dir.exists():
            data_dir.mkdir(parents=True, exist_ok=True)
            self._create_sample_documents()
            logger.info(f"Created sample documents in {data_dir}")
        
        # Load all documents
        txt_files = list(data_dir.glob("*.txt"))
        if not txt_files:
            logger.warning("No .txt files found, creating defaults")
            self._create_sample_documents()
            txt_files = list(data_dir.glob("*.txt"))
        
        for txt_file in txt_files:
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        self.documents.append(content)
            except Exception as e:
                logger.error(f"Error reading {txt_file}: {e}")
        
        if not self.documents:
            raise ValueError("No documents loaded - cannot index")
        
        # Create embeddings
        logger.info(f"Embedding {len(self.documents)} documents...")
        embeddings = self.embedding_gen.embed(self.documents)
        
        # Build FAISS index
        embedding_dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.index.add(embeddings.astype(np.float32))
        
        logger.info(f"✅ Indexed {len(self.documents)} documents in {embedding_dim}D space")
    
    def search(self, query: str, top_k: int = 5) -> List[str]:
        """
        Search for similar documents
        
        Args:
            query: Search query text
            top_k: Number of results to return
        
        Returns:
            List of matching documents
        """
        if not self.index or not self.documents:
            logger.warning("Vector store not initialized")
            return []
        
        try:
            # Embed query
            query_embedding = self.embedding_gen.embed([query])
            
            # Search
            distances, indices = self.index.search(query_embedding.astype(np.float32), top_k)
            
            # Get results
            results = [
                self.documents[i] for i in indices[0] 
                if i < len(self.documents)
            ]
            
            logger.debug(f"Search for '{query[:50]}...' returned {len(results)} results")
            return results
        
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    def _create_sample_documents(self):
        """Create default sample university documents"""
        samples = [
            "Admissions: Apply online at admissions.university.edu. Require SAT/ACT scores, GPA 3.5+, and essays.",
            "Tuition: Annual tuition is $45,000. Financial aid and scholarships available for qualified students.",
            "Academic Programs: BS Computer Science, MS Data Science, MBA, PhD Engineering, and more.",
            "Campus Life: 200-acre downtown campus with modern facilities, 24/7 library, student center.",
            "Student Life: 200+ clubs, sports teams, research opportunities, internships, and mentorship programs.",
            "Housing: On-campus and off-campus housing available. Housing office at housing@university.edu.",
            "Career Services: Resume reviews, interview prep, job fairs, internship placements, and alumni network.",
            "Research: Cutting-edge labs in AI, robotics, biotechnology, and renewable energy research."
        ]
        
        data_dir = Path("data/sample_documents")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        for i, sample in enumerate(samples):
            file_path = data_dir / f"document_{i}.txt"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(sample)
            logger.debug(f"Created {file_path}")
