# File: version_tracker.py
import csv
import os
from datetime import datetime
from pathlib import Path

class VersionTracker:
    def __init__(self, csv_path="project_versions.csv"):
        self.csv_path = Path(csv_path)
        self._initialize_csv()
    
    def _initialize_csv(self):
        if not self.csv_path.exists():
            with open(self.csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'version_id', 'timestamp', 'action', 
                    'files_affected', 'backup_path', 'tag'
                ])
    
    def record_action(self, action, files, backup_path="", tag=""):
        version_id = self._get_next_version_id()
        timestamp = datetime.now().isoformat()
        
        with open(self.csv_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                version_id,
                timestamp,
                action,
                ';'.join(files),
                backup_path,
                tag
            ])
        return version_id
    
    def _get_next_version_id(self):
        if not self.csv_path.exists():
            return 1
            
        with open(self.csv_path, 'r') as f:
            reader = csv.reader(f)
            return sum(1 for _ in reader)  # Count existing rows