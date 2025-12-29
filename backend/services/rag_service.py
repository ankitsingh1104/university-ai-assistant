"""RAG Service for document indexing and retrieval."""
import os
from typing import List, Dict, Any
import openai
from pinecone import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter

class RAGService:
    """Retrieval-Augmented Generation Service."""
    
    def __init__(self):
        """Initialize RAG service with Pinecone and OpenAI."""
        self.pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        self.index = self.pc.Index(os.getenv('PINECONE_INDEX', 'university-ai'))
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.chunk_size = int(os.getenv('CHUNK_SIZE', 500))
        self.chunk_overlap = int(os.getenv('CHUNK_OVERLAP', 50))
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
    
    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding from OpenAI."""
        response = openai.Embedding.create(
            input=text,
            model='text-embedding-ada-002'
        )
        return response['data'][0]['embedding']
    
    def index_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Index documents in vector database."""
        vectors = []
        for doc in documents:
            chunks = self.splitter.split_text(doc.get('content', ''))
            for i, chunk in enumerate(chunks):
                embedding = self._get_embedding(chunk)
                vectors.append((
                    f"{doc.get('id')}_chunk_{i}",
                    embedding,
                    {'text': chunk, 'doc_id': doc.get('id')}
                ))
        
        self.index.upsert(vectors=vectors)
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant documents from vector database."""
        query_embedding = self._get_embedding(query)
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        return results.get('matches', [])
