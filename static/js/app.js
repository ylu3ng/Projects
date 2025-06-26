// Global variables
let sessionId = null;
let isProcessing = false;
let hasReceivedFirstResponse = false;
let userName = '';

// DOM elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const chatForm = document.getElementById('chatForm');
const loadingIndicator = document.getElementById('loadingIndicator');
const sidebar = document.getElementById('sidebar');
const openSidebarBtn = document.getElementById('openSidebar');
const closeSidebarBtn = document.getElementById('closeSidebar');
const sessionIdSpan = document.getElementById('sessionId');
const messageCountSpan = document.getElementById('messageCount');
const sessionStartSpan = document.getElementById('sessionStart');
const studentNameSpan = document.getElementById('studentName');
const insightsList = document.getElementById('insightsList');
const exportSessionBtn = document.getElementById('exportSession');
const deleteSessionBtn = document.getElementById('deleteSession');
const nameModal = document.getElementById('nameModal');
const nameForm = document.getElementById('nameForm');
const userNameInput = document.getElementById('userNameInput');
const welcomeMessage = document.getElementById('welcomeMessage');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Show name input modal first
    showNameModal();
});

function showNameModal() {
    nameModal.style.display = 'flex';
    userNameInput.focus();
}

function hideNameModal() {
    nameModal.style.display = 'none';
}

function initializeApp() {
    // Generate a new session ID
    sessionId = generateSessionId();
    sessionIdSpan.textContent = sessionId;
    sessionStartSpan.textContent = new Date().toLocaleString();
    studentNameSpan.textContent = userName;
    
    // Show personalized welcome message
    showPersonalizedWelcome();
    
    // Auto-resize textarea
    messageInput.addEventListener('input', autoResizeTextarea);
    
    // Enable/disable send button based on input
    messageInput.addEventListener('input', toggleSendButton);
    
    // Initial button state
    toggleSendButton();
}

function showPersonalizedWelcome() {
    welcomeMessage.style.display = 'block';
    const welcomeTitle = welcomeMessage.querySelector('h3');
    const welcomeText = welcomeMessage.querySelector('p:last-child');
    
    // Update welcome message with user's name
    welcomeTitle.innerHTML = `Welcome, ${userName}! 🎓`;
    welcomeText.innerHTML = `Hi ${userName}! I'm here to help you with your math studies. Ask me anything - I'll guide you step-by-step through the solutions!`;
}

function setupEventListeners() {
    // Name form submission
    nameForm.addEventListener('submit', handleNameSubmit);
    
    // Chat form submission
    chatForm.addEventListener('submit', handleChatSubmit);
    
    // Sidebar controls
    openSidebarBtn.addEventListener('click', openSidebar);
    closeSidebarBtn.addEventListener('click', closeSidebar);
    
    // Session actions
    exportSessionBtn.addEventListener('click', exportSession);
    deleteSessionBtn.addEventListener('click', deleteSession);
    
    // Close sidebar when clicking outside
    document.addEventListener('click', function(e) {
        if (!sidebar.contains(e.target) && !openSidebarBtn.contains(e.target)) {
            closeSidebar();
        }
    });
    
    // Enter key handling (Shift+Enter for new line, Enter to send)
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!isProcessing && messageInput.value.trim()) {
                handleChatSubmit(e);
            }
        }
    });
}

function handleNameSubmit(e) {
    e.preventDefault();
    
    const name = userNameInput.value.trim();
    if (!name) {
        showNotification('Please enter your name', 'error');
        return;
    }
    
    // Store the user's name
    userName = name;
    
    // Hide modal and initialize app
    hideNameModal();
    initializeApp();
    setupEventListeners();
    
    // Show welcome notification
    showNotification(`Welcome, ${userName}! Let's start learning! 🎓`, 'success');
}

function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function autoResizeTextarea() {
    // Reset height to auto to get the correct scrollHeight
    messageInput.style.height = 'auto';
    
    // Calculate the new height based on content
    const scrollHeight = messageInput.scrollHeight;
    const minHeight = 44; // Minimum height in pixels
    const maxHeight = 120; // Maximum height in pixels
    
    // Set the height with constraints
    const newHeight = Math.max(minHeight, Math.min(scrollHeight, maxHeight));
    messageInput.style.height = newHeight + 'px';
    
    // Show scrollbar if content exceeds max height
    if (scrollHeight > maxHeight) {
        messageInput.style.overflowY = 'auto';
    } else {
        messageInput.style.overflowY = 'hidden';
    }
}

function toggleSendButton() {
    const hasText = messageInput.value.trim().length > 0;
    sendButton.disabled = !hasText || isProcessing;
}

function openSidebar() {
    sidebar.classList.add('open');
    updateSessionInfo();
}

function closeSidebar() {
    sidebar.classList.remove('open');
}

async function handleChatSubmit(e) {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message || isProcessing) return;
    
    // Add user message to chat
    addMessage('user', message);
    
    // Clear input and reset
    messageInput.value = '';
    autoResizeTextarea();
    toggleSendButton();
    
    // Show loading indicator
    showLoading();
    
    try {
        isProcessing = true;
        
        // Send message to backend with user name
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId,
                user_name: userName
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Hide loading indicator
        hideLoading();
        
        // Add AI response to chat
        addMessage('assistant', data.response);
        
        // Generate learning insights after first tutor response
        if (!hasReceivedFirstResponse) {
            hasReceivedFirstResponse = true;
            generateLearningInsights(data.response, message);
        }
        
        // Update session info
        updateSessionInfo();
        
    } catch (error) {
        console.error('Error sending message:', error);
        hideLoading();
        addMessage('assistant', `Sorry ${userName}, I encountered an error. Please try again.`);
    } finally {
        isProcessing = false;
        toggleSendButton();
    }
}

function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? '👤' : '🤖';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    
    // Process content based on role
    if (role === 'assistant') {
        // Process markdown and LaTeX
        bubble.innerHTML = processMarkdownAndLatex(content);
    } else {
        bubble.textContent = content;
    }
    
    const timestamp = document.createElement('span');
    timestamp.className = 'message-timestamp';
    timestamp.textContent = new Date().toLocaleTimeString();
    
    messageContent.appendChild(bubble);
    messageContent.appendChild(timestamp);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Render LaTeX after adding to DOM
    if (role === 'assistant') {
        renderLatex(messageDiv);
        highlightCode(messageDiv);
    }
}

function processMarkdownAndLatex(content) {
    // Configure marked.js for safe rendering
    marked.setOptions({
        breaks: true,
        gfm: true,
        sanitize: false,
        smartLists: true,
        smartypants: true
    });
    
    // Process markdown
    let processedContent = marked.parse(content);
    
    // Escape LaTeX content to prevent conflicts with markdown
    processedContent = processedContent.replace(/\\\(/g, '\\(').replace(/\\\)/g, '\\)');
    processedContent = processedContent.replace(/\\\[/g, '\\[').replace(/\\\]/g, '\\]');
    
    return processedContent;
}

function renderLatex(element) {
    // Render LaTeX in the element
    if (typeof renderMathInElement !== 'undefined') {
        renderMathInElement(element, {
            delimiters: [
                {left: '$$', right: '$$', display: true},
                {left: '$', right: '$', display: false},
                {left: '\\(', right: '\\)', display: false},
                {left: '\\[', right: '\\]', display: true}
            ],
            throwOnError: false
        });
    }
}

function highlightCode(element) {
    // Highlight code blocks with Prism.js
    if (typeof Prism !== 'undefined') {
        Prism.highlightAllUnder(element);
    }
}

function showLoading() {
    loadingIndicator.style.display = 'block';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideLoading() {
    loadingIndicator.style.display = 'none';
}

async function updateSessionInfo() {
    try {
        const response = await fetch(`/api/session/${sessionId}/summary`);
        if (response.ok) {
            const data = await response.json();
            messageCountSpan.textContent = data.message_count;
            
            // Update learning insights if available
            if (data.learning_insights && data.learning_insights.length > 0) {
                updateLearningInsights(data.learning_insights);
            }
        }
    } catch (error) {
        console.error('Error updating session info:', error);
    }
}

function updateLearningInsights(insights) {
    if (!insights || insights.length === 0) {
        insightsList.innerHTML = '<li class="no-insights">No insights yet. Start chatting to see what you learn!</li>';
        return;
    }
    
    insightsList.innerHTML = '';
    insights.forEach(insight => {
        const li = document.createElement('li');
        li.textContent = insight;
        insightsList.appendChild(li);
    });
}

function generateLearningInsights(tutorResponse, userQuestion) {
    // Create a summary of the learning session
    const insights = [];
    
    // Extract key concepts from the tutor's response
    const responseText = tutorResponse.toLowerCase();
    const questionText = userQuestion.toLowerCase();
    
    // Look for mathematical concepts
    const mathConcepts = [
        'derivative', 'integral', 'calculus', 'differentiation', 'integration',
        'probability', 'statistics', 'mean', 'median', 'mode', 'variance',
        'function', 'equation', 'formula', 'theorem', 'proof', 'solution',
        'optimization', 'maximize', 'minimize', 'critical point', 'limit',
        'series', 'sequence', 'convergence', 'divergence', 'matrix', 'vector'
    ];
    
    const foundConcepts = mathConcepts.filter(concept => 
        responseText.includes(concept) || questionText.includes(concept)
    );
    
    if (foundConcepts.length > 0) {
        insights.push(`📚 Learning about: ${foundConcepts.slice(0, 3).join(', ')}`);
    }
    
    // Look for problem-solving approaches
    if (responseText.includes('step') || responseText.includes('method')) {
        insights.push('🔍 Understanding problem-solving methodology');
    }
    
    if (responseText.includes('formula') || responseText.includes('equation')) {
        insights.push('📐 Working with mathematical formulas and equations');
    }
    
    if (responseText.includes('graph') || responseText.includes('plot')) {
        insights.push('📊 Learning about graphical representations');
    }
    
    // Add a general insight based on the question type
    if (questionText.includes('how') || questionText.includes('why')) {
        insights.push('🤔 Developing conceptual understanding');
    } else if (questionText.includes('solve') || questionText.includes('calculate')) {
        insights.push('🧮 Practicing computational skills');
    }
    
    // Update the insights display
    if (insights.length > 0) {
        updateLearningInsights(insights);
    }
}

async function exportSession() {
    try {
        const response = await fetch(`/api/session/${sessionId}/export`);
        if (response.ok) {
            const data = await response.json();
            
            // Create and download the file
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `math_tutor_session_${userName}_${sessionId}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            showNotification('Session exported successfully!', 'success');
        } else {
            throw new Error('Failed to export session');
        }
    } catch (error) {
        console.error('Error exporting session:', error);
        showNotification('Failed to export session', 'error');
    }
}

async function deleteSession() {
    if (!confirm(`Are you sure you want to delete this session, ${userName}? This action cannot be undone.`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/session/${sessionId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            // Reset the application
            sessionId = generateSessionId();
            sessionIdSpan.textContent = sessionId;
            sessionStartSpan.textContent = new Date().toLocaleString();
            hasReceivedFirstResponse = false;
            
            // Clear chat messages except welcome message
            const welcomeMessage = chatMessages.querySelector('.welcome-message');
            chatMessages.innerHTML = '';
            if (welcomeMessage) {
                chatMessages.appendChild(welcomeMessage);
            }
            
            // Reset insights
            updateLearningInsights([]);
            
            showNotification('Session deleted successfully!', 'success');
        } else {
            throw new Error('Failed to delete session');
        }
    } catch (error) {
        console.error('Error deleting session:', error);
        showNotification('Failed to delete session', 'error');
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 8px;
        color: #fff8e1;
        font-weight: 900;
        z-index: 10000;
        animation: slideIn 0.3s ease;
        max-width: 300px;
    `;
    
    // Set background color based on type
    if (type === 'success') {
        notification.style.background = '#348799';
    } else if (type === 'error') {
        notification.style.background = '#e57373';
    } else {
        notification.style.background = '#455a64';
    }
    
    // Add to page
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style); 