import json
from pathlib import Path
from datetime import datetime
from config import settings

class LocalSyncManager:
    def __init__(self):
        self.storage_dir = Path(settings.PROJECT_ROOT) / "sessions" / "local_sync"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
    def save_session(self, session_data):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"session_{timestamp}.json"
        filepath = self.storage_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump({
                "timestamp": timestamp,
                "data": session_data,
                "sync_status": "pending"
            }, f, indent=2)
        
        return {
            "status": "local_saved",
            "path": str(filepath),
            "message": "Saved locally for future sync"
        }

    def get_pending_sessions(self):
        return list(self.storage_dir.glob('*.json'))
