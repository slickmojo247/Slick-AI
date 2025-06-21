import json
from pathlib import Path
from datetime import datetime

class LocalSyncManager:
    def __init__(self, project_root):
        self.storage_dir = Path(project_root) / "sessions" / "local_store"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
    def save_session(self, session_data):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = self.storage_dir / f"session_{timestamp}.json"
        
        with open(filepath, 'w') as f:
            json.dump({
                "timestamp": timestamp,
                "data": session_data,
                "sync_status": "pending"
            }, f)
        
        return str(filepath)

    def get_pending_sessions(self):
        return list(self.storage_dir.glob('session_*.json'))
