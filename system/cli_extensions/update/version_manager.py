# system/version_manager.py
import os
import shutil
import json
from datetime import datetime
from pathlib import Path

class VersionManager:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        self.backup_dir = self.project_root / "system" / "backups"
        self.history_file = self.backup_dir / "version_history.json"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.history_file.exists():
            with open(self.history_file, "w") as f:
                json.dump({"versions": []}, f)

    def create_backup(self, file_path, source="vscode"):
        """Create timestamped backup with source metadata"""
        rel_path = Path(file_path).relative_to(self.project_root)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{timestamp}_{source}_{rel_path.name}"
        backup_path = self.backup_dir / rel_path.parent / backup_name
        
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)
        
        # Update version history
        with open(self.history_file, "r+") as f:
            history = json.load(f)
            history["versions"].append({
                "path": str(rel_path),
                "backup": str(backup_path),
                "timestamp": timestamp,
                "source": source,
                "hash": self.file_hash(file_path)
            })
            f.seek(0)
            json.dump(history, f, indent=2)
        
        return backup_path

    def file_hash(self, file_path):
        """Simple content-based hash for change detection"""
        import hashlib
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def get_previous_versions(self, file_path, limit=4):
        """Get last N versions of a file"""
        rel_path = str(Path(file_path).relative_to(self.project_root))
        with open(self.history_file, "r") as f:
            history = json.load(f)
        
        versions = [v for v in history["versions"] if v["path"] == rel_path]
        return sorted(versions, key=lambda x: x["timestamp"], reverse=True)[:limit]