#!/usr/bin/env python3
import os
import csv
from pathlib import Path
from datetime import datetime
import sys

class SlickCSVBackup:
    def __init__(self):
        self.base_dir = Path(__file__).parent.resolve()
        self.backup_dir = self.base_dir / "backup"
        self.log_dir = self.base_dir / "logs"
        self.setup_dirs()
        
    def setup_dirs(self):
        """Ensure required directories exist"""
        self.backup_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)
        
    def create_csv_backup(self, target=None):
        """Create CSV backup of file metadata and contents"""
        try:
            # Use provided target or default backup directory
            target_dir = Path(target) if target else self.backup_dir
            target_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = target_dir / f"slick_backup_{timestamp}.csv"
            log_file = self.log_dir / f"backup_log_{timestamp}.txt"
            
            # Essential directories to back up
            include_paths = [
                "core",
                "logic_engine",
                "config",
                "interfaces",
                "web",
                "system"
            ]
            
            # CSV headers
            fieldnames = [
                'file_path', 
                'file_size', 
                'modified_time',
                'content_sample',
                'backup_timestamp'
            ]
            
            with open(backup_file, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for path in include_paths:
                    full_path = self.base_dir / path
                    if full_path.exists():
                        if full_path.is_file():
                            self._write_file_to_csv(writer, full_path, timestamp)
                        else:
                            for root, _, files in os.walk(full_path):
                                for file in files:
                                    file_path = Path(root) / file
                                    self._write_file_to_csv(writer, file_path, timestamp)
            
            # Create log file
            with open(log_file, 'w') as f:
                f.write(f"CSV Backup created at {datetime.now()}\n")
                f.write(f"Backup location: {backup_file}\n")
                f.write(f"Included paths: {', '.join(include_paths)}\n")
            
            print(f"✅ CSV BACKUP SUCCESSFUL!")
            print(f"📍 Location: {backup_file}")
            print(f"📝 Log saved: {log_file}")
            return True
            
        except Exception as e:
            print(f"❌ CSV BACKUP FAILED: {str(e)}")
            return False

    def _write_file_to_csv(self, writer, file_path, timestamp):
        """Write individual file data to CSV"""
        try:
            # Get file metadata
            stat = file_path.stat()
            content_sample = ""
            
            # Read first 200 chars for text files
            if file_path.suffix in ['.py', '.txt', '.csv', '.html', '.js', '.css']:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content_sample = f.read(200)
                except:
                    content_sample = "[binary content]"
            
            writer.writerow({
                'file_path': str(file_path.relative_to(self.base_dir)),
                'file_size': stat.st_size,
                'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'content_sample': content_sample,
                'backup_timestamp': timestamp
            })
        except Exception as e:
            print(f"⚠️ Could not backup {file_path}: {str(e)}")

if __name__ == "__main__":
    backup = SlickCSVBackup()
    target = sys.argv[1] if len(sys.argv) > 1 else None
    backup.create_csv_backup(target)