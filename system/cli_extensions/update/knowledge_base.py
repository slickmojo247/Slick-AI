import json
import os
from datetime import datetime

class KnowledgeBase:
    def __init__(self, data_dir="think_sessions"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.sessions = {}
        self.load_sessions()
    
    def load_sessions(self):
        """Load all think sessions from disk"""
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".json"):
                session_id = filename[:-5]
                with open(os.path.join(self.data_dir, filename)) as f:
                    self.sessions[session_id] = json.load(f)
    
    def save_sessions(self):
        """Save all sessions to disk"""
        for session_id, content in self.sessions.items():
            with open(os.path.join(self.data_dir, f"{session_id}.json"), "w") as f:
                json.dump(content, f, indent=2)
    
    def query(self, topic):
        """Query sessions by topic"""
        results = []
        for session_id, content in self.sessions.items():
            if topic.lower() in content.get('title', '').lower() or \
               topic.lower() in content.get('content', '').lower():
                results.append({
                    "id": session_id,
                    "title": content.get('title', ''),
                    "excerpt": content.get('content', '')[:200] + "..."
                })
        return results
    
    def add_session(self, session_id, title, content):
        """Add a new think session"""
        self.sessions[session_id] = {
            "id": session_id,
            "title": title,
            "content": content,
            "created": datetime.now().isoformat()
        }