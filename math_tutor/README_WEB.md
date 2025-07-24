# AI Math Tutor Web Application

A modern web interface for your AI Math Tutor agent, featuring real-time chat, LaTeX rendering, code highlighting, and session management.

## Features

- 🤖 **AI Math Tutor**: Powered by Google's Gemini model with SymPy and Wolfram Alpha integration
- 💬 **Real-time Chat**: Clean, modern chat interface with typing indicators
- 📐 **LaTeX Rendering**: Beautiful mathematical notation using KaTeX
- 💻 **Code Highlighting**: Syntax highlighting for Python, JSON, and R code
- 📝 **Markdown Support**: Rich text formatting for responses
- 📊 **Session Management**: Track learning insights and export conversations
- 📱 **Responsive Design**: Works perfectly on desktop and mobile devices
- 🎨 **Modern UI**: Clean, gradient-based design with smooth animations

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Google AI Studio API key
- (Optional) Wolfram Alpha API key

### Installation

1. **Navigate to the Project Directory**
   ```bash
   cd math_tutor
   ```

2. **Create and Activate a Virtual Environment (using system Python)**
   ```bash
   /usr/bin/python3 -m venv sysvenv
   source sysvenv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set Up API Keys**
   - Set your environment variables:
     ```bash
     export GOOGLE_API_KEY="your_google_ai_studio_api_key"
     export WOLFRAM_ALPHA_APP_ID="your_wolfram_alpha_app_id"  # Optional
     ```

5. **Run the Application**
   ```bash
   python math_tutor_web.py
   ```
   - The app will be available at [http://localhost:8080](http://localhost:8080)

**Tip:**  
You can use the provided `setup.sh` script to automate steps 2 and 3:
```bash
bash setup.sh
```
Then activate your environment and continue from step 4.

## Project Structure

```
├── app.py                 # Flask web server
├── math_tutor_agent.py    # Your existing AI agent
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main web interface
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── app.js        # Frontend functionality
└── README_WEB.md         # This file
```

## API Endpoints

- `GET /` - Main chat interface
- `POST /api/chat` - Send a message to the AI tutor
- `GET /api/session/<session_id>/summary` - Get session summary and insights
- `GET /api/session/<session_id>/export` - Export session as JSON
- `DELETE /api/session/<session_id>` - Delete a session

## Usage

### Basic Chat
1. Type your math question in the input field
2. Press Enter or click the send button
3. The AI tutor will respond with step-by-step guidance

### Session Management
- Click the floating action button (⚙️) to open session info
- View learning insights automatically extracted from conversations
- Export your session as a JSON file for later review
- Delete sessions to start fresh

### Supported Input Formats
- Natural language: "Help me solve this integral"
- Mathematical notation: "∫ x² dx from 0 to 1"
- Equations: "Solve x² + 2x + 1 = 0"

## Deployment Options

### Local Development
Perfect for testing and personal use:
```bash
python app.py
```

### Cloud Deployment (Step-by-Step)

#### Option 1: Render (Recommended for beginners)

1. **Create a Render account** at [render.com](https://render.com)

2. **Create a new Web Service**:
   - Connect your GitHub repository
   - Choose Python as the runtime
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python app.py`

3. **Add environment variables**:
   - `GOOGLE_API_KEY`: Your Google AI Studio API key
   - `WOLFRAM_ALPHA_APP_ID`: Your Wolfram Alpha API key (optional)

4. **Deploy** and get your live URL!

#### Option 2: Railway

1. **Create a Railway account** at [railway.app](https://railway.app)

2. **Deploy from GitHub**:
   - Connect your repository
   - Railway will auto-detect Python
   - Add environment variables in the dashboard

3. **Your app will be live** with a Railway URL

#### Option 3: Heroku

1. **Create a Heroku account** and install Heroku CLI

2. **Create a Procfile** (create a file named `Procfile` with no extension):
   ```
   web: python app.py
   ```

3. **Deploy**:
   ```bash
   heroku create your-app-name
   heroku config:set GOOGLE_API_KEY=your_key
   git push heroku main
   ```

### Environment Variables

Set these in your deployment platform:

- `GOOGLE_API_KEY`: Required - Your Google AI Studio API key
- `WOLFRAM_ALPHA_APP_ID`: Optional - For enhanced mathematical computations
- `PORT`: Optional - Port number (usually auto-detected)

## Customization

### Styling
Edit `static/css/style.css` to customize:
- Colors and gradients
- Fonts and typography
- Layout and spacing
- Animations and transitions

### Functionality
Modify `static/js/app.js` to add:
- Custom keyboard shortcuts
- Additional UI features
- Integration with other services

### AI Behavior
Update `math_tutor_agent.py` to:
- Modify the system prompt
- Add new tools
- Change the AI model

## Troubleshooting

### Common Issues

1. **"Import error" for langchain_google_genai**
   ```bash
   pip install --upgrade langchain-google-genai
   ```

2. **"API key not found" error**
   - Ensure your `GOOGLE_API_KEY` environment variable is set
   - Check that the key is valid in Google AI Studio

3. **LaTeX not rendering**
   - Check browser console for JavaScript errors
   - Ensure KaTeX is loading properly

4. **Chat not working**
   - Check browser network tab for API errors
   - Verify the Flask server is running on the correct port

### Performance Tips

- Use a production WSGI server like Gunicorn for deployment
- Consider adding Redis for session storage in production
- Implement rate limiting for API endpoints
- Add caching for frequently requested computations

## Contributing

Feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

## License

This project is open source. Feel free to use and modify for your own projects.

## Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the browser console for errors
3. Check the Flask server logs
4. Create an issue with detailed error information

---

**Happy Learning! 🎓** 