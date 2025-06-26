# 🤖 AI Math Tutor - Interactive Learning Platform

A beautiful, personalized AI-powered math tutoring web application built with Flask and modern web technologies. Features a stunning Gaia theme with intelligent learning insights and personalized interactions.

## ✨ Features

### 🎨 Beautiful Gaia Theme
- **Modern Design**: Clean, elegant interface with a warm color palette
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile devices
- **Smooth Animations**: Engaging user experience with smooth transitions and hover effects
- **Custom Typography**: Beautiful fonts (Lato and Roboto Mono) for optimal readability

### 👤 Personalized Experience
- **Name-based Welcome**: Users enter their name for a personalized experience
- **Customized Interactions**: AI tutor addresses users by name throughout the session
- **Personalized Insights**: Learning insights are tailored to each individual student
- **Session Management**: Track progress with personalized session information

### 🧮 Advanced Math Support
- **LaTeX Rendering**: Beautiful mathematical notation with KaTeX
- **Code Highlighting**: Syntax highlighting for code examples with Prism.js
- **Markdown Support**: Rich text formatting for comprehensive explanations
- **Multiple Math Topics**: Support for calculus, statistics, algebra, geometry, and more

### 📊 Intelligent Learning Insights
- **Real-time Analysis**: Automatically generates insights after the first tutor response
- **Concept Detection**: Identifies mathematical concepts being learned
- **Progress Tracking**: Monitors learning patterns and difficulty levels
- **Personalized Feedback**: Insights are customized with the student's name

### 🔧 Smart Features
- **Dynamic Textarea**: Auto-resizes to fit content with smooth animations
- **Session Export**: Download complete chat sessions as JSON files
- **Session Management**: Create, track, and delete learning sessions
- **Real-time Updates**: Live session information and message counting

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Google AI Studio API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-math-tutor
   ```

2. **Set up environment variables**
   ```bash
   export GOOGLE_API_KEY="your_google_ai_studio_api_key_here"
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-cors
   ```

4. **Run the application**
   ```bash
   python math_tutor_web.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8080`

## 📁 Project Structure

```
ai-math-tutor/
├── math_tutor_web.py          # Main Flask application
├── math_tutor_agent.py        # AI agent implementation
├── templates/
│   └── index.html            # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css         # Gaia theme styles
│   └── js/
│       └── app.js            # Frontend JavaScript
└── README.md                 # This file
```

## 🎯 Key Components

### Frontend (HTML/CSS/JavaScript)
- **Responsive Design**: Mobile-first approach with CSS Grid and Flexbox
- **Interactive UI**: Smooth animations and real-time updates
- **Accessibility**: Keyboard navigation and screen reader support
- **Modern JavaScript**: ES6+ features with async/await patterns

### Backend (Python/Flask)
- **RESTful API**: Clean API endpoints for chat and session management
- **Session Storage**: In-memory session management (can be extended to database)
- **AI Integration**: Seamless integration with Google AI Studio
- **Personalization Engine**: Intelligent response personalization

### AI Features
- **Context Awareness**: Maintains conversation history for coherent responses
- **Mathematical Expertise**: Specialized in college-level mathematics
- **Learning Analytics**: Automatic insight generation and progress tracking
- **Adaptive Responses**: Personalized feedback based on user interaction

## 🎨 Theme Customization

The application uses a beautiful Gaia theme with the following color palette:

- **Primary**: `#348799` (Teal Blue)
- **Secondary**: `#0288d1` (Light Blue)
- **Background**: `#fff8e1` (Warm Cream)
- **Text**: `#455a64` (Dark Gray)
- **Accent**: `#e57373` (Soft Red)

### Customizing Colors
Edit `static/css/style.css` to modify the color scheme:

```css
:root {
    --primary-color: #348799;
    --secondary-color: #0288d1;
    --background-color: #fff8e1;
    --text-color: #455a64;
    --accent-color: #e57373;
}
```

## 📝 Description Locations

The following descriptions can be customized in the application:

### 1. Welcome Message
**Location**: `templates/index.html` (lines 40-50)
```html
<div class="welcome-message" id="welcomeMessage">
    <h3>Welcome to your AI Math Tutor! 🎓</h3>
    <p>I'm here to help you with:</p>
    <ul>
        <li>📊 Statistics and Probability</li>
        <li>🧮 Calculus and Integration</li>
        <li>📈 Mathematical Analysis</li>
        <li>🔢 Equation Solving</li>
    </ul>
    <p>Ask me anything - I'll guide you step-by-step through the solutions!</p>
</div>
```

### 2. Header Description
**Location**: `templates/index.html` (line 35)
```html
<p>Your personal tutor for college-level Statistics and Mathematics</p>
```

### 3. Modal Welcome
**Location**: `templates/index.html` (line 25)
```html
<h2>Welcome to AI Math Tutor! 🎓</h2>
```

### 4. Input Placeholder
**Location**: `templates/index.html` (line 65)
```html
placeholder="Ask your math question here..."
```

### 5. Loading Message
**Location**: `templates/index.html` (line 58)
```html
<p>AI Tutor is thinking...</p>
```

### 6. Sidebar Labels
**Location**: `templates/index.html` (lines 85-95)
```html
<label>Student:</label>
<label>Session ID:</label>
<label>Messages:</label>
<label>Started:</label>
```

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google AI Studio API key (required)

### Server Configuration
- **Host**: `0.0.0.0` (accessible from any IP)
- **Port**: `8080`
- **Debug Mode**: Enabled for development

### Session Management
- **Storage**: In-memory (sessions are lost on server restart)
- **Session ID**: Auto-generated with timestamp and random string
- **Export Format**: JSON with chat history and insights

## 🚀 Deployment

### Local Development
```bash
python math_tutor_web.py
```

### Production Deployment
1. Set up a production WSGI server (Gunicorn, uWSGI)
2. Configure environment variables
3. Set up reverse proxy (Nginx, Apache)
4. Enable HTTPS with SSL certificates

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "math_tutor_web.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google AI Studio** for providing the AI capabilities
- **KaTeX** for beautiful mathematical rendering
- **Prism.js** for code syntax highlighting
- **Marked.js** for Markdown processing
- **Lato Font** for beautiful typography

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code comments

---

**Made with ❤️ for better math education**
