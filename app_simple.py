from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import json
from datetime import datetime
import uuid

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
        
        # Demo mode responses (no AI agent import needed)
        ai_response = get_demo_response(message)
        
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

def get_demo_response(message):
    """Provide demo responses when AI agent is not available"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm your AI Math Tutor in demo mode. I can help you with math questions, but you'll need to set up your Google AI Studio API key for full functionality.\n\n**To get started:**\n1. Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)\n2. Set it as an environment variable: `export GOOGLE_API_KEY='your_key_here'`\n3. Restart the application"
    
    elif any(word in message_lower for word in ['integral', 'integration']):
        return "**Integration Example**\n\nLet me show you how to solve an integral step by step:\n\n**Problem:** Find $\\int x^2 dx$\n\n**Solution:**\n1. **Power Rule:** For $\\int x^n dx = \\frac{x^{n+1}}{n+1} + C$\n2. **Apply the rule:** $\\int x^2 dx = \\frac{x^3}{3} + C$\n\n**Answer:** $\\frac{x^3}{3} + C$\n\n*Note: This is a demo response. Set up your API key for real-time calculations!*"
    
    elif any(word in message_lower for word in ['derivative', 'differentiate']):
        return "**Derivative Example**\n\nLet's find the derivative of $f(x) = x^3 + 2x^2 + 5x + 1$\n\n**Solution:**\n1. **Power Rule:** $\\frac{d}{dx}[x^n] = nx^{n-1}$\n2. **Apply to each term:**\n   - $\\frac{d}{dx}[x^3] = 3x^2$\n   - $\\frac{d}{dx}[2x^2] = 4x$\n   - $\\frac{d}{dx}[5x] = 5$\n   - $\\frac{d}{dx}[1] = 0$\n3. **Combine:** $f'(x) = 3x^2 + 4x + 5$\n\n**Answer:** $f'(x) = 3x^2 + 4x + 5$\n\n*Note: This is a demo response. Set up your API key for real-time calculations!*"
    
    elif any(word in message_lower for word in ['equation', 'solve']):
        return "**Equation Solving Example**\n\nLet's solve: $x^2 - 4x + 4 = 0$\n\n**Solution:**\n1. **Recognize perfect square:** $(x-2)^2 = x^2 - 4x + 4$\n2. **Set to zero:** $(x-2)^2 = 0$\n3. **Take square root:** $x-2 = 0$\n4. **Solve:** $x = 2$\n\n**Answer:** $x = 2$ (double root)\n\n*Note: This is a demo response. Set up your API key for real-time calculations!*"
    
    elif any(word in message_lower for word in ['statistics', 'probability']):
        return "**Statistics Example**\n\nLet's calculate the mean of the dataset: $[2, 4, 6, 8, 10]$\n\n**Solution:**\n1. **Sum the values:** $2 + 4 + 6 + 8 + 10 = 30$\n2. **Count the values:** $n = 5$\n3. **Calculate mean:** $\\bar{x} = \\frac{30}{5} = 6$\n\n**Answer:** The mean is $6$\n\n*Note: This is a demo response. Set up your API key for real-time calculations!*"
    
    else:
        return "I'm your AI Math Tutor in demo mode! I can help you with:\n\n- **Calculus:** Integration, differentiation, limits\n- **Algebra:** Equation solving, factoring, functions\n- **Statistics:** Probability, mean, variance, distributions\n- **And much more!**\n\n**To get full functionality:**\n1. Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)\n2. Set it as an environment variable: `export GOOGLE_API_KEY='your_key_here'`\n3. Restart the application\n\nTry asking me about integrals, derivatives, equations, or statistics!"

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
    print("🚀 Starting AI Math Tutor Web Application...")
    print("📱 Open your browser to: http://localhost:8080")
    print("🎨 Featuring the beautiful Gaia theme!")
    print("🔧 Running in demo mode - no API key required!")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=8080) 