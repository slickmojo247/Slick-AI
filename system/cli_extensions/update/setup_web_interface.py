import os
from pathlib import Path

WEB_INTERFACE_FILES = {
    'web_interface/__init__.py': '',
    'web_interface/app.py': """
from flask import Flask, render_template, request, jsonify
from slick.system.boot_loader import boot_system
from engine.logic_core import SlickLogicEngine
import threading

app = Flask(__name__)
engine = SlickLogicEngine()

init_thread = threading.Thread(target=boot_system)
init_thread.start()

@app.route('/')
def index():
    return render_template('index.html', ai_name="Slick")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    response = engine.handle_command(user_input)
    return jsonify({'response': response})

@app.route('/voice', methods=['POST'])
def voice():
    return jsonify({'status': 'Voice endpoint active'})

def run_web_server():
    app.run(host='0.0.0.0', port=5000, debug=True)
""",
    'web_interface/templates/index.html': """
<!DOCTYPE html>
<html>
<head>
    <title>Slick AI Interface</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="chat-container">
        <h1>{{ ai_name }} AI Assistant</h1>
        <div id="chat-box"></div>
        <div class="input-area">
            <input type="text" id="user-input" placeholder="Ask me anything...">
            <button id="send-btn">Send</button>
        </div>
    </div>
    <script src="/static/script.js"></script>
</body>
</html>
""",
    'web_interface/static/style.css': """
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #1a2a6c, #b21f1f, #1a2a6c);
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
    color: white;
}

.chat-container {
    width: 800px;
    height: 600px;
    background: rgba(0, 0, 0, 0.7);
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    backdrop-filter: blur(10px);
}
""",
    'web_interface/static/script.js': """
document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    
    function addMessage(text, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'ai-message');
        messageDiv.textContent = text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        addMessage(message, true);
        userInput.value = '';
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            addMessage(data.response);
        } catch (error) {
            addMessage('Error connecting to AI server');
        }
    }
    
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    
    setTimeout(() => {
        addMessage('Hello! I\\'m Slick, your personal AI assistant. How can I help you today?');
    }, 1000);
});
"""
}

def setup_web_interface():
    for path, content in WEB_INTERFACE_FILES.items():
        filepath = Path(path)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        if not filepath.exists():
            with open(filepath, 'w') as f:
                f.write(content.strip())
            print(f"Created: {path}")
        else:
            print(f"Exists: {path} - skipping")

if __name__ == '__main__':
    print("Setting up web interface...")
    setup_web_interface()
    print("\nNext steps:")
    print("1. Install dependencies: pip install flask")
    print("2. Run: python3 SLICK.py")
    print("3. Access the web interface at http://localhost:5000")