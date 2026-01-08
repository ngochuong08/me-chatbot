"""
Flask API Server - REST API cho chatbot
Sử dụng cho Node.js web interface
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.chatbot import MEChatbot

app = Flask(__name__)
CORS(app)  # Enable CORS for Node.js frontend

# Initialize chatbot
print("Initializing ME Chatbot...")
chatbot = MEChatbot(
    documents_path="./documents",
    vector_db_path="./vector_db",
    use_local_llm=False  # Change to True if using vLLM local
)

# Store conversations in memory (in production, use Redis or database)
conversations = {}


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "ME Chatbot API"
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint"""
    try:
        data = request.json
        message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id', 'default')
        
        if not message:
            return jsonify({
                "error": "Message is required"
            }), 400
        
        # Get or create conversation
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        # Chat with bot
        result = chatbot.chat(message)
        
        # Store in conversation history
        conversations[conversation_id].append({
            "role": "user",
            "content": message
        })
        conversations[conversation_id].append({
            "role": "assistant",
            "content": result['answer'],
            "sources": result['sources']
        })
        
        return jsonify({
            "answer": result['answer'],
            "sources": result['sources'],
            "conversation_id": conversation_id
        })
    
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route('/api/search', methods=['POST'])
def search():
    """Search documents endpoint"""
    try:
        data = request.json
        query = data.get('query', '').strip()
        k = data.get('k', 5)
        
        if not query:
            return jsonify({
                "error": "Query is required"
            }), 400
        
        results = chatbot.search_documents(query, k=k)
        
        # Format results
        formatted_results = []
        for doc in results:
            formatted_results.append({
                "filename": doc.metadata.get('filename', 'Unknown'),
                "content": doc.page_content,
                "source": doc.metadata.get('source', '')
            })
        
        return jsonify({
            "results": formatted_results,
            "count": len(formatted_results)
        })
    
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route('/api/compare', methods=['POST'])
def compare():
    """Compare documents endpoint"""
    try:
        data = request.json
        file1 = data.get('file1', '').strip()
        file2 = data.get('file2', '').strip()
        
        if not file1 or not file2:
            return jsonify({
                "error": "Both file paths are required"
            }), 400
        
        result = chatbot.compare_documents(file1, file2)
        
        if 'error' in result:
            return jsonify({
                "error": result['error']
            }), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route('/api/upload', methods=['POST'])
def upload():
    """Upload document endpoint"""
    try:
        if 'file' not in request.files:
            return jsonify({
                "error": "No file provided"
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                "error": "No file selected"
            }), 400
        
        # Save file
        filename = file.filename
        filepath = os.path.join('./documents', filename)
        file.save(filepath)
        
        # Add to vector store
        chatbot.add_document(filepath)
        
        return jsonify({
            "status": "success",
            "message": f"Document uploaded and indexed: {filename}",
            "filename": filename
        })
    
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route('/api/conversations/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get conversation history"""
    if conversation_id not in conversations:
        return jsonify({
            "error": "Conversation not found"
        }), 404
    
    return jsonify({
        "conversation_id": conversation_id,
        "messages": conversations[conversation_id]
    })


@app.route('/api/conversations/<conversation_id>/reset', methods=['POST'])
def reset_conversation(conversation_id):
    """Reset conversation"""
    if conversation_id in conversations:
        conversations[conversation_id] = []
    
    chatbot.reset_conversation()
    
    return jsonify({
        "status": "success",
        "message": "Conversation reset"
    })


@app.route('/api/rebuild', methods=['POST'])
def rebuild_vector_store():
    """Rebuild vector store from documents folder"""
    try:
        chatbot.rebuild_vector_store()
        return jsonify({
            "status": "success",
            "message": "Vector store rebuilt"
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == '__main__':
    # Create documents folder
    os.makedirs('./documents', exist_ok=True)
    
    print("\n" + "="*60)
    print("ME Chatbot API Server")
    print("="*60)
    print("\nAPI Endpoints:")
    print("  POST /api/chat              - Chat with bot")
    print("  POST /api/search            - Search documents")
    print("  POST /api/compare           - Compare documents")
    print("  POST /api/upload            - Upload document")
    print("  GET  /api/conversations/:id - Get conversation")
    print("  POST /api/conversations/:id/reset - Reset conversation")
    print("  POST /api/rebuild           - Rebuild vector store")
    print("\n" + "="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
