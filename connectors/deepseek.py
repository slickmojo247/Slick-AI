import requests
import json
import socket
from pathlib import Path
from datetime import datetime
from config import settings
import time

class DeepSeekConnector:
    def __init__(self):
        self.endpoint = "https://api.deepseek.ai/v1"
        self.max_retries = 2
        self.timeout = 5
        self.local_backup_dir = Path(settings.PROJECT_ROOT) / "sessions" / "pending_sync"
        self.local_backup_dir.mkdir(parents=True, exist_ok=True)
        self.valid_dns = False
        self._check_dns()

    def _check_dns(self):
        try:
            socket.gethostbyname('api.deepseek.ai')
            self.valid_dns = True
        except socket.gaierror:
            self.valid_dns = False

    def sync_session(self, session_file):
        if not self.valid_dns:
            print("⚠️ DNS resolution failed - using local storage")
            return self._store_locally(session_file)

        try:
            with open(session_file, 'r') as f:
                session_content = f.read()
                
            backup_path = self._store_locally(session_file)['path']
            
            response = requests.post(
                f"{self.endpoint}/session/sync",
                json={"session_data": session_content},
                headers={
                    "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            
            Path(backup_path).unlink()  # Remove backup after successful sync
            return response.json()
            
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"⚠️ Sync failed: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "local_backup": backup_path
            }

    def _store_locally(self, session_file):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = self.local_backup_dir / f"pending_{timestamp}.json"
        
        with open(session_file, 'r') as src, open(backup_file, 'w') as dst:
            dst.write(src.read())
            
        return {
            "status": "stored_locally",
            "path": str(backup_file),
            "message": "Will sync when connection is available"
        }
