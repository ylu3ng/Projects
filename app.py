from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import json
from datetime import datetime
import uuid

# Import your existing math tutor agent
from math_tutor_agent import agent_executor, HumanMessage, AIMessage

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for chat sessions (in production, use a database)
chat_sessions = {}

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        session_id = data.get('session_id')
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get or create session
        if session_id not in chat_sessions:
            chat_sessions[session_id] = {
                'chat_history': [],
                'created_at': datetime.now().isoformat(),
                'learning_insights': []
            }
        
        session = chat_sessions[session_id]
        
        # Add user message to history
        session['chat_history'].append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Get response from agent
        response = agent_executor.invoke({
            "input": message,
            "chat_history": session['chat_history']
        })
        
        ai_response = response["output"]
        
        # Add AI response to history
        session['chat_history'].append({
            'role': 'assistant',
            'content': ai_response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Extract learning insights (simple keyword-based approach)
        insights = extract_learning_insights(ai_response)
        if insights:
            session['learning_insights'].extend(insights)
        
        return jsonify({
            'response': ai_response,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/session/<session_id>/summary', methods=['GET'])
def get_session_summary(session_id):
    """Get learning insights summary for a session"""
    if session_id not in chat_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    session = chat_sessions[session_id]
    return jsonify({
        'session_id': session_id,
        'created_at': session['created_at'],
        'message_count': len(session['chat_history']),
        'learning_insights': list(set(session['learning_insights'])),  # Remove duplicates
        'chat_history': session['chat_history']
    })

@app.route('/api/session/<session_id>/export', methods=['GET'])
def export_session(session_id):
    """Export chat session as JSON"""
    if session_id not in chat_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    session = chat_sessions[session_id]
    export_data = {
        'session_id': session_id,
        'created_at': session['created_at'],
        'exported_at': datetime.now().isoformat(),
        'chat_history': session['chat_history'],
        'learning_insights': list(set(session['learning_insights']))
    }
    
    return jsonify(export_data)

@app.route('/api/session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a chat session"""
    if session_id in chat_sessions:
        del chat_sessions[session_id]
        return jsonify({'message': 'Session deleted successfully'})
    return jsonify({'error': 'Session not found'}), 404

def extract_learning_insights(response):
    """Extract learning insights from AI response"""
    insights = []
    
    # Simple keyword-based extraction
    keywords = [
        'concept', 'principle', 'formula', 'theorem', 'definition',
        'integration', 'differentiation', 'probability', 'statistics',
        'optimization', 'derivative', 'integral', 'function'
    ]
    
    response_lower = response.lower()
    for keyword in keywords:
        if keyword in response_lower:
            insights.append(f"Learned about {keyword}")
    
    return insights

if __name__ == '__main__':
    # Check for required environment variables
    if not os.environ.get('GOOGLE_API_KEY'):
        print("Warning: GOOGLE_API_KEY environment variable not set!")
        print("Please set your Google AI Studio API key before running the app.")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 