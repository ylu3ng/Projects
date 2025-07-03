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

# Configuration for learning insights
INSIGHT_CONFIG = {
    'use_llm_enhancement': True,  # Set to False to use only concept-based insights
    'max_insights': 5,
    'llm_timeout': 10  # seconds
}

# Comprehensive mathematical concept taxonomy
MATH_CONCEPTS = {
    'calculus': {
        'keywords': ['derivative', 'integral', 'differentiation', 'integration', 'limit', 'continuity', 'differentiable', 'antiderivative'],
        'subtopics': ['limits', 'derivatives', 'integrals', 'applications', 'series', 'multivariable'],
        'difficulty_levels': ['basic', 'intermediate', 'advanced']
    },
    'statistics': {
        'keywords': ['probability', 'mean', 'median', 'mode', 'variance', 'standard deviation', 'distribution', 'hypothesis', 'confidence'],
        'subtopics': ['descriptive', 'inferential', 'probability', 'regression', 'sampling'],
        'difficulty_levels': ['basic', 'intermediate', 'advanced']
    },
    'algebra': {
        'keywords': ['equation', 'function', 'polynomial', 'quadratic', 'linear', 'system', 'matrix', 'vector', 'eigenvalue'],
        'subtopics': ['linear algebra', 'abstract algebra', 'number theory', 'group theory'],
        'difficulty_levels': ['basic', 'intermediate', 'advanced']
    },
    'geometry': {
        'keywords': ['area', 'volume', 'perimeter', 'triangle', 'circle', 'rectangle', 'polygon', 'coordinate', 'transformation'],
        'subtopics': ['euclidean', 'analytic', 'differential', 'topology'],
        'difficulty_levels': ['basic', 'intermediate', 'advanced']
    },
    'trigonometry': {
        'keywords': ['sine', 'cosine', 'tangent', 'angle', 'trigonometric', 'unit circle', 'identity', 'inverse'],
        'subtopics': ['right triangles', 'unit circle', 'identities', 'equations'],
        'difficulty_levels': ['basic', 'intermediate', 'advanced']
    },
    'graph_theory': {
        'keywords': ['graph', 'vertex', 'edge', 'degree', 'sequence', 'handshaking', 'theorem', 'lemma', 'path', 'cycle', 'tree', 'connected'],
        'subtopics': ['basic concepts', 'theorems', 'algorithms', 'applications'],
        'difficulty_levels': ['basic', 'intermediate', 'advanced']
    },
    'optimization': {
        'keywords': ['maximize', 'minimize', 'critical point', 'extrema', 'optimization', 'constraint', 'lagrange'],
        'subtopics': ['linear programming', 'nonlinear', 'constrained', 'global vs local'],
        'difficulty_levels': ['intermediate', 'advanced']
    },
    'series': {
        'keywords': ['sequence', 'series', 'convergence', 'divergence', 'summation', 'taylor', 'maclaurin', 'power'],
        'subtopics': ['arithmetic', 'geometric', 'power series', 'fourier'],
        'difficulty_levels': ['intermediate', 'advanced']
    },
    'differential_equations': {
        'keywords': ['differential equation', 'ode', 'pde', 'initial value', 'boundary value', 'separable', 'homogeneous'],
        'subtopics': ['first order', 'second order', 'systems', 'partial differential'],
        'difficulty_levels': ['intermediate', 'advanced']
    },
    'number_theory': {
        'keywords': ['prime', 'factorization', 'gcd', 'lcm', 'modular arithmetic', 'congruence', 'theorem'],
        'subtopics': ['divisibility', 'primes', 'congruences', 'diophantine'],
        'difficulty_levels': ['intermediate', 'advanced']
    },
    'discrete_math': {
        'keywords': ['combinatorics', 'permutation', 'combination', 'graph', 'tree', 'algorithm', 'recursion'],
        'subtopics': ['combinatorics', 'graph theory', 'logic', 'set theory'],
        'difficulty_levels': ['basic', 'intermediate', 'advanced']
    }
}

# Import the math tutor agent for learning insights
try:
    from math_tutor_agent import agent_executor
    from langchain_core.messages import HumanMessage, AIMessage
    MATH_AGENT_AVAILABLE = True
    print("Math tutor agent imported successfully for learning insights")
except ImportError as e:
    print(f"Math tutor agent not available for learning insights: {e}")
    MATH_AGENT_AVAILABLE = False

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
            insights = generate_hybrid_learning_insights(message, personalized_response, user_name)
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
    """Personalize the AI response with the user's name in a natural way"""
    if not user_name or user_name.lower() in ['user', 'student', 'anonymous']:
        return response
    
    personalized = response
    
    # Only add name in greetings and specific contexts, not randomly throughout
    if any(word in response.lower() for word in ['hello', 'hi', 'welcome', 'greetings']):
        # Add name to greetings naturally
        if 'hello' in response.lower():
            personalized = response.replace('Hello', f'Hello, {user_name}')
        elif 'hi' in response.lower():
            personalized = response.replace('Hi', f'Hi, {user_name}')
        elif 'welcome' in response.lower():
            personalized = response.replace('Welcome', f'Welcome, {user_name}')
    
    # Remove the overly aggressive name replacement
    # Don't replace every "you" with "you, {user_name}" - that's unnatural
    
    # Only add encouraging phrases if the response is positive and doesn't already have encouragement
    # But make it more natural and less frequent
    if any(word in response.lower() for word in ['correct', 'right', 'good', 'excellent', 'perfect']) and not any(word in response.lower() for word in ['great', 'excellent', 'good job']):
        # Only add encouragement 30% of the time to avoid overuse
        import random
        if random.random() < 0.3:
            encouraging_phrases = [
                f"Great question!",
                f"Excellent thinking!",
                f"Keep it up!",
                f"You're doing great!"
            ]
            
            encouragement = random.choice(encouraging_phrases)
            if encouragement not in personalized:
                personalized += f"\n\n{encouragement}"
    
    return personalized

def generate_agent_based_insights(user_question, tutor_response, user_name):
    """Generate learning insights using the math tutor agent"""
    if not MATH_AGENT_AVAILABLE:
        return []
    
    try:
        # Create a context for the agent about the learning session
        context = f"""
        Student Question: {user_question}
        Tutor Response: {tutor_response}
        Student Name: {user_name}
        
        Based on this interaction, what has the student learned? Please provide 2-3 specific insights about:
        1. The mathematical concepts they worked with
        2. The problem-solving techniques they used
        3. Their learning progress and understanding
        
        Focus on concrete, actionable insights that would help track their learning journey.
        """
        
        # Use the agent to generate insights
        response = agent_executor.invoke({
            "input": f"What have I learned from this interaction? {context}",
            "chat_history": []
        })
        
        ai_message_content = response["output"]
        
        # Parse the agent's response into structured insights
        insights = []
        lines = ai_message_content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('AI Tutor:'):
                # Clean up the response and format as insights
                if any(keyword in line.lower() for keyword in ['learned', 'understood', 'worked with', 'practiced', 'developed']):
                    insights.append(f"📚 {user_name} {line}")
                elif any(keyword in line.lower() for keyword in ['concept', 'technique', 'method', 'approach']):
                    insights.append(f"🔍 {user_name} {line}")
                elif any(keyword in line.lower() for keyword in ['progress', 'improvement', 'growth', 'development']):
                    insights.append(f"📈 {user_name} {line}")
        
        return insights[:3]  # Limit to 3 insights
        
    except Exception as e:
        print(f"Error generating agent-based insights: {e}")
        return []

def generate_hybrid_learning_insights(user_question, tutor_response, user_name):
    """Generate hybrid learning insights using both concept tags and agent enhancement"""
    insights = []
    
    # Step 1: Generate concept-based insights (fast and reliable)
    concept_insights = generate_concept_based_insights(user_question, tutor_response, user_name)
    insights.extend(concept_insights)
    
    # Step 2: Generate learning summary (comprehensive overview)
    detected_concepts = []
    for insight in concept_insights:
        if 'is learning about:' in insight:
            concepts = insight.split('is learning about: ')[-1]
            detected_concepts.append(concepts)
    
    learning_summary = generate_learning_summary(user_question, tutor_response, user_name, detected_concepts)
    if learning_summary:
        # Add summary as a special insight
        summary_text = " ".join(learning_summary[:2])  # Take first two parts
        insights.append(f"📖 {user_name}'s learning summary: {summary_text}")
    
    # Step 3: Generate agent-based insights (using math_tutor_agent)
    if MATH_AGENT_AVAILABLE and INSIGHT_CONFIG['use_llm_enhancement']:
        try:
            agent_insights = generate_agent_based_insights(user_question, tutor_response, user_name)
            insights.extend(agent_insights)
        except Exception as e:
            print(f"Agent insight generation failed: {e}")
            # Fallback to LLM-enhanced insights
            try:
                llm_insights = generate_llm_enhanced_insights(user_question, tutor_response, user_name, concept_insights)
                insights.extend(llm_insights)
            except Exception as e2:
                print(f"LLM insight generation also failed: {e2}")
    
    # Step 4: Remove duplicates and limit to top insights
    unique_insights = list(set(insights))
    return unique_insights[:INSIGHT_CONFIG['max_insights']]

def generate_concept_based_insights(user_question, tutor_response, user_name):
    """Generate insights based on mathematical concept detection from tutor's response"""
    insights = []
    
    question_lower = user_question.lower()
    response_lower = tutor_response.lower()
    combined_text = f"{question_lower} {response_lower}"
    
    # Enhanced concept detection based on tutor's actual explanation
    detected_concepts = []
    concept_details = {}
    
    for concept, data in MATH_CONCEPTS.items():
        # Check if the tutor actually explained this concept
        concept_keywords = data['keywords']
        explained_keywords = []
        
        for keyword in concept_keywords:
            if keyword in response_lower:
                explained_keywords.append(keyword)
        
        if explained_keywords:
            detected_concepts.append(concept)
            concept_details[concept] = explained_keywords
    
    if detected_concepts:
        unique_concepts = list(set(detected_concepts))[:3]  # Top 3 concepts
        insights.append(f"📚 {user_name} is learning about: {', '.join(unique_concepts)}")
        
        # Add specific concept insights based on what the tutor actually explained
        for concept in unique_concepts[:2]:  # Limit to 2 specific insights
            if concept in concept_details:
                specific_keywords = concept_details[concept][:2]  # Top 2 keywords
                if specific_keywords:
                    insights.append(f"🔍 {user_name} is working with {concept} concepts: {', '.join(specific_keywords)}")
    
    # Detect specific mathematical techniques the tutor explained
    techniques_detected = []
    
    if any(word in response_lower for word in ['power rule', 'chain rule', 'product rule', 'quotient rule']):
        techniques_detected.append('differentiation rules')
    
    if any(word in response_lower for word in ['substitution', 'integration by parts', 'partial fractions']):
        techniques_detected.append('integration techniques')
    
    if any(word in response_lower for word in ['factoring', 'completing the square', 'quadratic formula']):
        techniques_detected.append('algebraic methods')
    
    if any(word in response_lower for word in ['normal distribution', 'binomial', 'poisson', 'uniform']):
        techniques_detected.append('probability distributions')
    
    if any(word in response_lower for word in ['hypothesis test', 'confidence interval', 'p-value']):
        techniques_detected.append('statistical inference')
    
    # Graph theory specific techniques
    if any(word in response_lower for word in ['handshaking theorem', 'handshaking lemma', 'degree sum']):
        techniques_detected.append('graph theory theorems')
    
    if any(word in response_lower for word in ['degree sequence', 'vertex degree', 'edge count']):
        techniques_detected.append('graph analysis')
    
    if techniques_detected:
        insights.append(f"📐 {user_name} is learning specific techniques: {', '.join(techniques_detected[:2])}")
    
    # Detect problem-solving approach based on tutor's explanation
    if any(word in response_lower for word in ['step', 'method', 'approach', 'strategy', 'process', 'procedure']):
        insights.append(f"🔍 {user_name} is understanding problem-solving methodology")
    
    if any(word in response_lower for word in ['formula', 'equation', 'expression', 'theorem', 'rule']):
        insights.append(f"📐 {user_name} is working with mathematical formulas and equations")
    
    if any(word in response_lower for word in ['graph', 'plot', 'visualize', 'sketch', 'diagram', 'curve']):
        insights.append(f"📊 {user_name} is learning about graphical representations")
    
    if any(word in response_lower for word in ['proof', 'theorem', 'definition', 'lemma', 'corollary']):
        insights.append(f"📖 {user_name} is understanding mathematical proofs and definitions")
    
    # Question type analysis based on what the tutor actually addressed
    if any(word in question_lower for word in ['how', 'why', 'explain', 'understand', 'concept', 'what is']):
        insights.append(f"🤔 {user_name} is developing conceptual understanding")
    elif any(word in question_lower for word in ['solve', 'calculate', 'compute', 'find', 'evaluate', 'determine']):
        insights.append(f"🧮 {user_name} is practicing computational skills")
    elif any(word in question_lower for word in ['prove', 'show', 'demonstrate', 'verify', 'establish']):
        insights.append(f"🔬 {user_name} is learning proof techniques")
    
    # Difficulty level detection based on tutor's explanation complexity
    difficulty_indicators = {
        'basic': ['basic', 'fundamental', 'elementary', 'simple', 'introductory', 'first', 'start'],
        'intermediate': ['intermediate', 'moderate', 'standard', 'typical', 'common', 'usual'],
        'advanced': ['advanced', 'complex', 'sophisticated', 'challenging', 'difficult', 'higher-order', 'multiple']
    }
    
    for level, indicators in difficulty_indicators.items():
        if any(word in response_lower for word in indicators):
            if level == 'basic':
                insights.append(f"📝 {user_name} is building foundational knowledge")
            elif level == 'advanced':
                insights.append(f"🚀 {user_name} is tackling advanced mathematical concepts")
            break
    
    # Application context detection
    if any(word in question_lower for word in ['real', 'world', 'application', 'practical', 'use', 'where']):
        insights.append(f"🌍 {user_name} is connecting math to real-world applications")
    
    # Remove duplicates and limit insights
    unique_insights = list(set(insights))
    return unique_insights[:4]  # Limit to 4 insights for better focus

def generate_learning_summary(user_question, tutor_response, user_name, detected_concepts):
    """Generate a comprehensive learning summary based on the interaction"""
    summary_parts = []
    
    # Extract key concepts and theorems mentioned
    response_lower = tutor_response.lower()
    
    # Graph theory specific summary
    if 'graph' in response_lower and any(word in response_lower for word in ['degree', 'edge', 'vertex']):
        if 'handshaking' in response_lower:
            summary_parts.append("Key concepts in Graph Theory:")
            summary_parts.append("- Definition of vertices, degrees and edges in a graph")
            summary_parts.append("- Edges is the sum of degrees divided by 2 based on the handshaking theorem")
        else:
            summary_parts.append("Key concepts in Graph Theory:")
            summary_parts.append("- Understanding of graph structure and relationships")
            summary_parts.append("- Analysis of degree sequences and edge counting")
    
    # Calculus specific summary
    elif any(word in response_lower for word in ['derivative', 'integral']):
        if 'power rule' in response_lower:
            summary_parts.append("Key concepts in Calculus:")
            summary_parts.append("- Understanding of derivatives and the power rule")
            summary_parts.append("- Application of differentiation techniques")
        elif 'integration' in response_lower:
            summary_parts.append("Key concepts in Calculus:")
            summary_parts.append("- Understanding of integrals and integration techniques")
            summary_parts.append("- Application of anti-differentiation")
    
    # Statistics specific summary
    elif any(word in response_lower for word in ['probability', 'distribution', 'mean', 'variance']):
        summary_parts.append("Key concepts in Statistics:")
        summary_parts.append("- Understanding of probability distributions")
        summary_parts.append("- Analysis of statistical measures and relationships")
    
    # Algebra specific summary
    elif any(word in response_lower for word in ['equation', 'factor', 'solve']):
        summary_parts.append("Key concepts in Algebra:")
        summary_parts.append("- Understanding of equation solving techniques")
        summary_parts.append("- Application of algebraic methods and factoring")
    
    # General summary if no specific area detected
    else:
        summary_parts.append("Key mathematical concepts:")
        summary_parts.append("- Problem-solving methodology and mathematical reasoning")
        summary_parts.append("- Understanding of fundamental mathematical principles")
    
    return summary_parts

def generate_llm_enhanced_insights(user_question, tutor_response, user_name, concept_insights):
    """Generate LLM-enhanced insights for more contextual and personalized feedback"""
    try:
        # Extract detected concepts and techniques for context
        detected_concepts = []
        specific_techniques = []
        
        for insight in concept_insights:
            if 'is learning about:' in insight:
                concepts = insight.split('is learning about: ')[-1]
                detected_concepts.append(concepts)
            elif 'is working with' in insight and 'concepts:' in insight:
                # Extract specific concepts like "derivatives, integrals"
                technique_part = insight.split('concepts: ')[-1]
                specific_techniques.extend(technique_part.split(', '))
            elif 'is learning specific techniques:' in insight:
                techniques = insight.split('is learning specific techniques: ')[-1]
                specific_techniques.extend(techniques.split(', '))
        
        # Create a more focused prompt based on what the tutor actually explained
        prompt = f"""
        You are an expert math tutor analyzing a learning interaction. Generate 2-3 personalized, encouraging insights for {user_name}.

        CONTEXT:
        - Student Question: "{user_question[:200]}..."
        - Tutor Response: "{tutor_response[:300]}..."
        - Mathematical Areas: {', '.join(detected_concepts) if detected_concepts else 'General mathematics'}
        - Specific Techniques: {', '.join(specific_techniques) if specific_techniques else 'General problem-solving'}

        REQUIREMENTS:
        1. Focus on the specific mathematical concepts and techniques the tutor actually explained
        2. Be encouraging and motivating
        3. Keep each insight under 80 characters
        4. Start each insight with an appropriate emoji
        5. Reference the actual mathematical content discussed
        6. Use {user_name}'s name naturally (not in every sentence)

        EXAMPLE FORMAT (based on actual content):
        💡 {user_name} is mastering the power rule for derivatives
        🎯 {user_name} shows strong understanding of integration techniques
        ⭐ {user_name} grasps the fundamental concepts well

        Generate only the insights, one per line:
        """
        
        # Use the existing agent to generate insights
        response = agent_executor.invoke({
            "input": prompt,
            "chat_history": []
        })
        
        # Parse the response into individual insights
        llm_response = response["output"]
        insights = []
        
        # Split by lines and clean up
        for line in llm_response.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith(('1.', '2.', '3.', '-', '*', 'EXAMPLE', 'REQUIREMENTS', 'CONTEXT')):
                # Ensure it has an emoji and is personalized
                if not any(emoji in line for emoji in ['📚', '🔍', '📐', '📊', '📖', '🤔', '🧮', '🔬', '📝', '🚀', '🌍', '💡', '🎯', '⭐', '🌟', '🎓', '✨', '🔥', '💪', '🎉']):
                    line = f"💡 {line}"
                if user_name not in line:
                    line = line.replace('the student', user_name).replace('Student', user_name)
                insights.append(line)
        
        return insights[:2]  # Limit to 2 LLM insights for better focus
        
    except Exception as e:
        print(f"Error generating LLM insights: {e}")
        return []

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

@app.route('/api/insights/config', methods=['GET', 'POST'])
def insights_config():
    """Get or update learning insights configuration"""
    if request.method == 'GET':
        return jsonify(INSIGHT_CONFIG)
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            if 'use_llm_enhancement' in data:
                INSIGHT_CONFIG['use_llm_enhancement'] = data['use_llm_enhancement']
            if 'max_insights' in data:
                INSIGHT_CONFIG['max_insights'] = data['max_insights']
            
            return jsonify({
                'message': 'Configuration updated successfully',
                'config': INSIGHT_CONFIG
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400

@app.route('/api/insights/test', methods=['POST'])
def test_insights():
    """Test insight generation with sample data"""
    try:
        data = request.get_json()
        user_question = data.get('question', 'How do I find the derivative of x^2?')
        tutor_response = data.get('response', 'To find the derivative of x^2, you use the power rule...')
        user_name = data.get('user_name', 'Test User')
        
        # Generate insights
        insights = generate_hybrid_learning_insights(user_question, tutor_response, user_name)
        
        return jsonify({
            'question': user_question,
            'response': tutor_response,
            'user_name': user_name,
            'insights': insights,
            'config': INSIGHT_CONFIG
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Check for required environment variables
    if not os.environ.get('GOOGLE_API_KEY'):
        print("Warning: GOOGLE_API_KEY environment variable not set!")
        print("Please set your Google AI Studio API key before running the app.")
    
    print("🚀 Starting AI Math Tutor Web Application...")
    print("📱 Open your browser to: http://localhost:8080")
    print("🎨 Featuring the beautiful Gaia theme!")
    print("🧠 Enhanced with hybrid learning insights!")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=8080) 