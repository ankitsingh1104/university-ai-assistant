"""API routes for University AI Assistant."""
from flask import Blueprint, request, jsonify
from backend.services.rag_service import RAGService
from backend.services.chat_service import ChatService
from backend.services.search_service import SemanticSearchService

api_bp = Blueprint('api', __name__, url_prefix='/api')

rag_service = RAGService()
chat_service = ChatService()
search_service = SemanticSearchService()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200

@api_bp.route('/search', methods=['POST'])
def search():
    """Semantic search endpoint."""
    data = request.get_json()
    query = data.get('query')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    results = search_service.search(query)
    return jsonify({'results': results}), 200

@api_bp.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint with RAG."""
    data = request.get_json()
    message = data.get('message')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    response = chat_service.process_message(message)
    return jsonify({'response': response}), 200

@api_bp.route('/index', methods=['POST'])
def index_documents():
    """Index documents endpoint."""
    data = request.get_json()
    documents = data.get('documents', [])
    
    if not documents:
        return jsonify({'error': 'Documents are required'}), 400
    
    rag_service.index_documents(documents)
    return jsonify({'message': 'Documents indexed successfully'}), 200
