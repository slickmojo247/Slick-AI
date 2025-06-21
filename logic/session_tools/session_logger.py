import csv
import os
from datetime import datetime
from pathlib import Path

class SessionLogger:
    def __init__(self, project_root):
        self.project_root = Path(project_root).absolute()
        self.session_file = self.project_root / "sessions" / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Create directory if not exists
        self.session_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write header if new file
        if not self.session_file.exists():
            with open(self.session_file, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(["Step","Timestamp","Prompt","Response","File_Reference","Tags","Comments"])

    def log_step(self, prompt, response, file_ref, tags, comments=""):
        # Convert all paths to absolute
        abs_file_ref = (self.project_root / file_ref).absolute() if file_ref else None
        rel_file_ref = str(abs_file_ref.relative_to(self.project_root)) if abs_file_ref and abs_file_ref.exists() else file_ref
        
        with open(self.session_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([
                sum(1 for _ in open(self.session_file)),
                datetime.now().isoformat(),
                prompt,
                response,
                rel_file_ref,
                ",".join(tags) if isinstance(tags, list) else tags,
                comments
            ])
