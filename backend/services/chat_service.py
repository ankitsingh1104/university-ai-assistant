"""Chat Service for conversational AI."""
import os
from typing import List, Dict, Any
import openai
from backend.services.rag_service import RAGService

class ChatService:
    """Chat service with RAG integration."""
    
    def __init__(self):
        """Initialize chat service."""
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.rag_service = RAGService()
        self.model = 'gpt-3.5-turbo'
        self.conversation_history = []
    
    def _build_context(self, query: str) -> str:
        """Build context from RAG retrieval."""
        results = self.rag_service.retrieve(query, top_k=5)
        context = "\n".join([
            f"- {result.get('metadata', {}).get('text', '')}"
            for result in results
        ])
        return context
    
    def _build_system_prompt(self, context: str) -> str:
        """Build system prompt with context."""
        return f"""You are a helpful university AI assistant. 
Use the following context to answer questions:

{context}

Provide accurate, concise, and helpful responses."""
    
    def process_message(self, message: str) -> str:
        """Process user message and return response."""
        context = self._build_context(message)
        system_prompt = self._build_system_prompt(context)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        assistant_message = response['choices'][0]['message']['content']
        return assistant_message
    
    def reset_conversation(self) -> None:
        """Reset conversation history."""
        self.conversation_history = []
