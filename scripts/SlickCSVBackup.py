#!/usr/bin/env python3
import os
import csv
from pathlib import Path
from datetime import datetime
import sys

class SlickCSVBackup:
    """
    Manages the creation of CSV backups for the Slick AI project.
    It backs up file metadata (path, size, modified time) and
    a content sample for specified directories within the project.
    """
    def __init__(self):
        # Determine the base directory of the project.
        # This assumes the script is run from the project root or its immediate subdirectory.
        # We need to find the actual project root, not just the script's directory.
        # A robust way is to look for a marker file like 'main.py' or 'README.md'
        # or rely on the user running it from the root.
        # For simplicity, assuming this script will be placed at scripts/slick_backup.py
        # and base_dir should be the parent of 'scripts'.
        self.project_root = self._find_project_root()
        if not self.project_root:
            print("Error: Could not determine project root. Please run this script from the project's root directory or its 'scripts' subdirectory.")
            sys.exit(1)

        self.backup_dir = self.project_root / "backup"
        self.log_dir = self.project_root / "logs"
        self.setup_dirs()
        
    def _find_project_root(self):
        """
        Attempts to find the project's root directory by looking for a known marker
        (e.g., 'core' directory) relative to the script's location or its parent.
        """
        current_dir = Path(__file__).parent.resolve()
        # Check current directory
        if (current_dir / "core").exists() or (current_dir / "README.md").exists():
            return current_dir
        # Check parent directory (if script is in 'scripts/')
        if (current_dir.parent / "core").exists() or (current_dir.parent / "README.md").exists():
            return current_dir.parent
        return None

    def setup_dirs(self):
        """Ensure required backup and log directories exist."""
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            self.log_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Error setting up directories: {e}")
            sys.exit(1)
        
    def create_csv_backup(self, target=None):
        """
        Create CSV backup of file metadata and contents for specified project directories.
        
        Args:
            target (str, optional): An optional path to a custom backup directory.
                                    If None, uses the default 'backup/' directory.
        """
        try:
            # Use provided target or default backup directory
            target_dir = Path(target) if target else self.backup_dir
            target_dir.mkdir(parents=True, exist_ok=True) # Ensure target dir exists
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = target_dir / f"slick_backup_{timestamp}.csv"
            log_file = self.log_dir / f"backup_log_{timestamp}.txt"
            
            # Essential directories to back up (relative to project_root)
            # These are the top-level directories in your project structure
            include_paths = [
                "core",
                "logic_engine",
                "config",
                "interfaces",
                "web",
                "system",
                "scripts", # Include scripts directory itself
                "data"     # Assuming 'data' directory for CSVs like Slick_AI.csv
            ]
            
            # CSV headers
            fieldnames = [
                'file_path', 
                'file_size', 
                'modified_time',
                'content_sample',
                'backup_timestamp'
            ]
            
            with open(backup_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for path_name in include_paths:
                    full_path = self.project_root / path_name
                    if full_path.exists():
                        if full_path.is_file(): # Handle cases where path is a file (e.g., main.py)
                            self._write_file_to_csv(writer, full_path, timestamp)
                        elif full_path.is_dir():
                            for root, _, files in os.walk(full_path):
                                for file in files:
                                    file_path = Path(root) / file
                                    # Skip common ignored files like __pycache__ within scanned directories
                                    if "__pycache__" not in str(file_path) and not file.endswith(('.pyc', '.bak', '.log')):
                                        self._write_file_to_csv(writer, file_path, timestamp)
                        else:
                            print(f"⚠️ Warning: Path not found or not a file/directory: {full_path}")
                    else:
                        print(f"⚠️ Warning: Included path does not exist: {full_path.relative_to(self.project_root)}")
            
            # Create log file
            with open(log_file, 'w', encoding='utf-8') as f:
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
        """Write individual file data to CSV, handling encoding errors."""
        try:
            # Get file metadata
            stat = file_path.stat()
            content_sample = ""
            
            # Read first 200 chars for text files, handle encoding errors
            if file_path.suffix in ['.py', '.txt', '.csv', '.html', '.js', '.css', '.json', '.md', '.yaml', '.yml', '.ini', '.xml']:
                try:
                    # Attempt to read with utf-8, fallback to latin-1 if utf-8 fails
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content_sample = f.read(200)
                except UnicodeDecodeError:
                    try:
                        with open(file_path, 'r', encoding='latin-1') as f:
                            content_sample = f.read(200)
                    except Exception:
                        content_sample = "[unreadable text content]"
                except Exception:
                    content_sample = "[could not read text content]"
            else:
                content_sample = "[binary content]" # Mark non-text files as binary
            
            # Escape content sample to avoid issues with CSV delimiters within content
            content_sample = content_sample.replace('"', '""')

            writer.writerow({
                'file_path': str(file_path.relative_to(self.project_root)),
                'file_size': stat.st_size,
                'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'content_sample': content_sample,
                'backup_timestamp': timestamp
            })
        except Exception as e:
            print(f"⚠️ Could not backup file {file_path.relative_to(self.project_root)}: {str(e)}")

if __name__ == "__main__":
    backup = SlickCSVBackup()
    # If an argument is provided, use it as the target backup directory.
    # Otherwise, use the default internal backup directory.
    target = sys.argv[1] if len(sys.argv) > 1 else None
    backup.create_csv_backup(target)
