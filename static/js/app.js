// Global variables
let sessionId = null;
let isProcessing = false;

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
const insightsList = document.getElementById('insightsList');
const exportSessionBtn = document.getElementById('exportSession');
const deleteSessionBtn = document.getElementById('deleteSession');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
});

function initializeApp() {
    // Generate a new session ID
    sessionId = generateSessionId();
    sessionIdSpan.textContent = sessionId;
    sessionStartSpan.textContent = new Date().toLocaleString();
    
    // Auto-resize textarea
    messageInput.addEventListener('input', autoResizeTextarea);
    
    // Enable/disable send button based on input
    messageInput.addEventListener('input', toggleSendButton);
    
    // Initial button state
    toggleSendButton();
}

function setupEventListeners() {
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

function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function autoResizeTextarea() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
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
        
        // Send message to backend
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
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
        
        // Update session info
        updateSessionInfo();
        
    } catch (error) {
        console.error('Error sending message:', error);
        hideLoading();
        addMessage('assistant', 'Sorry, I encountered an error. Please try again.');
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
        gfm: true
    });
    
    // Process markdown
    let processedContent = marked.parse(content);
    
    // Ensure code blocks are properly formatted for Prism.js
    processedContent = processedContent.replace(
        /<pre><code class="language-(\w+)">/g,
        '<pre><code class="language-$1">'
    );
    
    return processedContent;
}

function renderLatex(element) {
    // Render LaTeX in the element
    renderMathInElement(element, {
        delimiters: [
            {left: '$$', right: '$$', display: true},
            {left: '$', right: '$', display: false},
            {left: '\\(', right: '\\)', display: false},
            {left: '\\[', right: '\\]', display: true}
        ],
        throwOnError: false,
        errorColor: '#cc0000'
    });
}

function highlightCode(element) {
    // Highlight code blocks with Prism.js
    const codeBlocks = element.querySelectorAll('pre code');
    codeBlocks.forEach(block => {
        Prism.highlightElement(block);
    });
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
            
            // Update learning insights
            updateLearningInsights(data.learning_insights);
        }
    } catch (error) {
        console.error('Error updating session info:', error);
    }
}

function updateLearningInsights(insights) {
    insightsList.innerHTML = '';
    
    if (insights && insights.length > 0) {
        insights.forEach(insight => {
            const li = document.createElement('li');
            li.textContent = insight;
            insightsList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.className = 'no-insights';
        li.textContent = 'No insights yet. Start chatting to see what you learn!';
        insightsList.appendChild(li);
    }
}

async function exportSession() {
    try {
        const response = await fetch(`/api/session/${sessionId}/export`);
        if (response.ok) {
            const data = await response.json();
            
            // Create and download file
            const blob = new Blob([JSON.stringify(data, null, 2)], {
                type: 'application/json'
            });
            
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `math-tutor-session-${sessionId}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            // Show success message
            showNotification('Session exported successfully!', 'success');
        }
    } catch (error) {
        console.error('Error exporting session:', error);
        showNotification('Failed to export session', 'error');
    }
}

async function deleteSession() {
    if (!confirm('Are you sure you want to delete this session? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/session/${sessionId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            // Reset the application
            location.reload();
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
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        animation: slideIn 0.3s ease;
        max-width: 300px;
    `;
    
    // Set background color based on type
    if (type === 'success') {
        notification.style.background = '#48bb78';
    } else if (type === 'error') {
        notification.style.background = '#e53e3e';
    } else {
        notification.style.background = '#667eea';
    }
    
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
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