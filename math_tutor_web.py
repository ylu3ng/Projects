from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import json
from datetime import datetime
import uuid
import re

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
        user_name = data.get('user_name', 'Student')
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get or create session
        if session_id not in chat_sessions:
            chat_sessions[session_id] = {
                'chat_history': [],
                'created_at': datetime.now().isoformat(),
                'learning_insights': [],
                'has_first_response': False,
                'user_name': user_name
            }
        else:
            # Update user name if provided
            chat_sessions[session_id]['user_name'] = user_name
        
        session = chat_sessions[session_id]
        
        # Add user message to history
        session['chat_history'].append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Create personalized prompt for the AI
        personalized_message = f"Hi {user_name}! {message}"
        
        # Get response from agent
        response = agent_executor.invoke({
            "input": personalized_message,
            "chat_history": session['chat_history']
        })
        
        ai_response = response["output"]
        
        # Personalize the AI response
        personalized_response = personalize_response(ai_response, user_name)
        
        # Add AI response to history
        session['chat_history'].append({
            'role': 'assistant',
            'content': personalized_response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Generate learning insights after first tutor response
        if not session['has_first_response']:
            session['has_first_response'] = True
            insights = generate_learning_insights(message, personalized_response, user_name)
            if insights:
                session['learning_insights'] = insights
        
        return jsonify({
            'response': personalized_response,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def personalize_response(response, user_name):
    """Personalize the AI response with the user's name"""
    # Add personal touches to the response
    personalized = response
    
    # Add greeting if it's the first interaction
    if not any(greeting in response.lower() for greeting in ['hello', 'hi', 'hey', 'welcome']):
        # Add a personal greeting at the beginning
        personalized = f"Hi {user_name}! {response}"
    
    # Replace generic references with personal ones
    personalized = personalized.replace('you', f'you, {user_name}')
    personalized = personalized.replace('your', f'your, {user_name}')
    
    # Add encouraging phrases
    encouraging_phrases = [
        f"Great question, {user_name}!",
        f"Well done, {user_name}!",
        f"Excellent thinking, {user_name}!",
        f"Keep it up, {user_name}!",
        f"You're doing great, {user_name}!"
    ]
    
    # Add encouragement at the end if the response is positive
    if any(word in response.lower() for word in ['correct', 'right', 'good', 'excellent', 'perfect']):
        import random
        encouragement = random.choice(encouraging_phrases)
        if encouragement not in personalized:
            personalized += f"\n\n{encouragement}"
    
    return personalized

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
        'learning_insights': session['learning_insights'],
        'chat_history': session['chat_history'],
        'user_name': session.get('user_name', 'Student')
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
        'learning_insights': session['learning_insights'],
        'user_name': session.get('user_name', 'Student')
    }
    
    return jsonify(export_data)

@app.route('/api/session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a chat session"""
    if session_id in chat_sessions:
        del chat_sessions[session_id]
        return jsonify({'message': 'Session deleted successfully'})
    return jsonify({'error': 'Session not found'}), 404

def generate_learning_insights(user_question, tutor_response, user_name):
    """Generate intelligent learning insights from the first tutor response"""
    insights = []
    
    # Convert to lowercase for easier matching
    question_lower = user_question.lower()
    response_lower = tutor_response.lower()
    
    # Mathematical concepts and topics
    math_concepts = {
        'calculus': ['derivative', 'integral', 'differentiation', 'integration', 'limit', 'continuity'],
        'statistics': ['probability', 'mean', 'median', 'mode', 'variance', 'standard deviation', 'distribution'],
        'algebra': ['equation', 'function', 'polynomial', 'quadratic', 'linear'],
        'geometry': ['area', 'volume', 'perimeter', 'triangle', 'circle', 'rectangle'],
        'trigonometry': ['sine', 'cosine', 'tangent', 'angle', 'trigonometric'],
        'optimization': ['maximize', 'minimize', 'critical point', 'extrema', 'optimization'],
        'series': ['sequence', 'series', 'convergence', 'divergence', 'summation'],
        'linear_algebra': ['matrix', 'vector', 'eigenvalue', 'determinant', 'linear transformation']
    }
    
    # Find relevant mathematical concepts
    found_concepts = []
    for category, concepts in math_concepts.items():
        for concept in concepts:
            if concept in question_lower or concept in response_lower:
                found_concepts.append(category)
                break
    
    if found_concepts:
        unique_concepts = list(set(found_concepts))  # Remove duplicates
        insights.append(f"📚 {user_name} is learning about: {', '.join(unique_concepts[:3])}")
    
    # Problem-solving approaches
    if any(word in response_lower for word in ['step', 'method', 'approach', 'strategy']):
        insights.append(f"🔍 {user_name} is understanding problem-solving methodology")
    
    if any(word in response_lower for word in ['formula', 'equation', 'expression']):
        insights.append(f"📐 {user_name} is working with mathematical formulas and equations")
    
    if any(word in response_lower for word in ['graph', 'plot', 'visualize', 'sketch']):
        insights.append(f"📊 {user_name} is learning about graphical representations")
    
    if any(word in response_lower for word in ['proof', 'theorem', 'definition']):
        insights.append(f"📖 {user_name} is understanding mathematical proofs and definitions")
    
    # Question type analysis
    if any(word in question_lower for word in ['how', 'why', 'explain', 'understand']):
        insights.append(f"🤔 {user_name} is developing conceptual understanding")
    elif any(word in question_lower for word in ['solve', 'calculate', 'compute', 'find']):
        insights.append(f"🧮 {user_name} is practicing computational skills")
    elif any(word in question_lower for word in ['prove', 'show', 'demonstrate']):
        insights.append(f"🔬 {user_name} is learning proof techniques")
    
    # Difficulty level indicators
    if any(word in response_lower for word in ['advanced', 'complex', 'sophisticated']):
        insights.append(f"🚀 {user_name} is tackling advanced mathematical concepts")
    elif any(word in response_lower for word in ['basic', 'fundamental', 'elementary']):
        insights.append(f"📝 {user_name} is building foundational knowledge")
    
    # Application context
    if any(word in question_lower for word in ['real', 'world', 'application', 'practical']):
        insights.append(f"🌍 {user_name} is connecting math to real-world applications")
    
    # Return unique insights (remove duplicates)
    return list(set(insights))

if __name__ == '__main__':
    # Check for required environment variables
    if not os.environ.get('GOOGLE_API_KEY'):
        print("Warning: GOOGLE_API_KEY environment variable not set!")
        print("Please set your Google AI Studio API key before running the app.")
    
    print("🚀 Starting AI Math Tutor Web Application...")
    print("📱 Open your browser to: http://localhost:8080")
    print("🎨 Featuring the beautiful Gaia theme!")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=8080) 