import os
import csv
import json

def create_project_structure():
    # Create root directory
    root_dir = "SLICK_Project"
    os.makedirs(root_dir, exist_ok=True)
    
    # Parse project_structure.csv
    with open('project_structure.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            path = os.path.join(root_dir, row['Path'])
            if row['Type'] == 'Directory':
                os.makedirs(os.path.join(path, row['Name']), exist_ok=True)
            elif row['Type'] == 'File':
                file_path = os.path.join(path, row['Name'])
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(row['Content'].replace('""', '"'))

def create_additional_files():
    # Create slick/web_interface/templates/index.html
    web_templates = "SLICK_Project/slick/web_interface/templates"
    os.makedirs(web_templates, exist_ok=True)
    with open(os.path.join(web_templates, 'index.html'), 'w') as f:
        f.write("""<!DOCTYPE html>
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
</html>""")

    # Create slick/web_interface/static files
    web_static = "SLICK_Project/slick/web_interface/static"
    os.makedirs(web_static, exist_ok=True)
    
    # style.css
    with open(os.path.join(web_static, 'style.css'), 'w') as f:
        f.write("""/* CSS for chat interface */
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

h1 {
    text-align: center;
    padding: 20px;
    background: rgba(0, 0, 0, 0.4);
    margin: 0;
    font-size: 28px;
    border-bottom: 1px solid #444;
}

#chat-box {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
}

.message {
    max-width: 70%;
    padding: 12px 18px;
    margin-bottom: 15px;
    border-radius: 18px;
    line-height: 1.5;
}

.user-message {
    align-self: flex-end;
    background: linear-gradient(to right, #0062ff, #00c3ff);
    border-bottom-right-radius: 5px;
}

.ai-message {
    align-self: flex-start;
    background: linear-gradient(to right, #333, #555);
    border-bottom-left-radius: 5px;
}

.input-area {
    display: flex;
    padding: 20px;
    background: rgba(0, 0, 0, 0.4);
    border-top: 1px solid #444;
}

#user-input {
    flex: 1;
    padding: 15px;
    border: none;
    border-radius: 30px;
    background: rgba(255, 255, 255, 0.1);
    color: white;
    font-size: 16px;
    outline: none;
}

#send-btn {
    background: linear-gradient(to right, #00c3ff, #0062ff);
    color: white;
    border: none;
    border-radius: 30px;
    padding: 0 30px;
    margin-left: 10px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s;
}

#send-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px #00c3ff;
}""")

    # script.js
    with open(os.path.join(web_static, 'script.js'), 'w') as f:
        f.write("""// JavaScript for chat functionality
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
    
    // Initial greeting
    setTimeout(() => {
        addMessage('Hello! I\\'m Slick, your personal AI assistant. How can I help you today?');
    }, 1000);
});""")

    # Create slick/data files
    data_dir = "SLICK_Project/slick/data"
    os.makedirs(data_dir, exist_ok=True)
    
    # ai_preferences_details.csv
    with open(os.path.join(data_dir, 'ai_preferences_details.csv'), 'w') as f:
        f.write("tone,humor_level,proactiveness,feedback_frequency,memory_decay_alpha,memory_decay_beta,memory_decay_gamma,contextual_recall_weights\n")
        f.write("professional_but_friendly,medium,medium,on_request,0.15,0.12,0.03,\"[0.5, 0.3, 0.2]\"")
    
    # memory_nodes.csv
    with open(os.path.join(data_dir, 'memory_nodes.csv'), 'w') as f:
        f.write("event_id,timestamp,sensory_context,emotional_weight,embeddings_type\n")
        f.write("evt001,2023-10-26T10:00:00Z,\"{""type"": ""audio"", ""source"": ""microphone""}\",0.7,str\n")
        f.write("evt002,2023-10-26T11:00:00Z,\"{""type"": ""visual"", ""source"": ""camera""}\",0.9,list")
    
    # profile_details.csv
    with open(os.path.join(data_dir, 'profile_details.csv'), 'w') as f:
        f.write("name,cognitive_preferences_learning_style,cognitive_preferences_memory_bias,personality_traits_curiosity,personality_traits_analytical,interests,habits,health_metrics_sleep_avg,privacy_settings_data_retention,privacy_settings_share_anonymous_data\n")
        f.write("Slick,visual,recent,0.9,0.8,AI research;quantum physics;system design,daily learning;coding,7.5,365_days,False")
    
    # snapshot_config.json
    with open(os.path.join(data_dir, 'snapshot_config.json'), 'w') as f:
        json.dump({
            "ai_profile": {
                "name": "Slick",
                "cognitive_preferences": {
                    "learning_style": "visual",
                    "memory_bias": "recent"
                },
                "personality_traits": {
                    "curiosity": 0.9,
                    "analytical": 0.8
                },
                "interests": [
                    "AI research",
                    "quantum physics",
                    "system design"
                ],
                "habits": [
                    "daily learning",
                    "coding"
                ],
                "health_metrics": {
                    "sleep_avg": 7.5
                },
                "privacy_settings": {
                    "data_retention": "365_days",
                    "share_anonymous_data": False
                }
            },
            "ai_preferences": {
                "tone": "professional_but_friendly",
                "humor_level": "medium",
                "proactiveness": "medium",
                "feedback_frequency": "on_request",
                "memory_decay_alpha": 0.15,
                "memory_decay_beta": 0.12,
                "memory_decay_gamma": 0.03,
                "contextual_recall_weights": [0.5, 0.3, 0.2]
            }
        }, f, indent=2)

if __name__ == '__main__':
    create_project_structure()
    create_additional_files()
    print("Project structure created successfully in SLICK_Project directory!")