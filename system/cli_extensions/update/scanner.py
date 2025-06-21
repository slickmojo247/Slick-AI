"""
SLICK AI - Comprehensive Directory Scanner with Color Tagging
Scans an entire directory structure and classifies files for UPDATE, MERGE, KEEP, or DELETE
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple
from enum import Enum, auto
import sqlite3
import csv

class FileAction(Enum):
    KEEP = auto()    # Green - Store/keep important files
    UPDATE = auto()  # Blue - Files needing updates
    MERGE = auto()   # Purple - Files to be merged
    DELETE = auto()  # Red - Files to delete
    REVIEW = auto()  # Pink - Needs manual review

class DirectoryScanner:
    """Comprehensive scanner with color tagging system"""
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.color_map = {
            FileAction.KEEP: "#4ADE80",   # Green
            FileAction.UPDATE: "#60A5FA", # Blue
            FileAction.MERGE: "#A78BFA",  # Purple
            FileAction.DELETE: "#F87171", # Red
            FileAction.REVIEW: "#F472B6"  # Pink
        }
        self._init_db()
    
    def _init_db(self):
        """Initialize the database for storing scan results"""
        self.db_path = self.root_path / "file_actions.db"
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS file_actions (
                path TEXT PRIMARY KEY,
                action TEXT,
                color TEXT,
                size INTEGER,
                last_modified REAL,
                notes TEXT
            )""")
    
    def scan_directory(self) -> Dict[str, Dict]:
        """Scan the entire directory structure"""
        results = {}
        
        for root, dirs, files in os.walk(self.root_path):
            # Skip hidden directories and special folders
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {'__pycache__', 'node_modules'}]
            
            current_path = Path(root)
            
            # First process directories
            for dir_name in dirs:
                dir_path = current_path / dir_name
                action = self._determine_action(dir_path)
                results[str(dir_path)] = self._create_record(dir_path, action)
            
            # Then process files
            for file_name in files:
                file_path = current_path / file_name
                action = self._determine_action(file_path)
                results[str(file_path)] = self._create_record(file_path, action)
        
        self._save_results_to_db(results)
        return results
    
    def _determine_action(self, path: Path) -> FileAction:
        """Determine the appropriate action for a file/directory"""
        # Directory-specific rules
        if path.is_dir():
            if path.name in {'legacy', 'old', 'archive', 'deprecated'}:
                return FileAction.DELETE
            if path.name in {'temp', 'tmp', 'cache'}:
                return FileAction.DELETE
            if path.name in {'merge', 'combined'}:
                return FileAction.MERGE
            if path.name in {'core', 'src', 'main'}:
                return FileAction.KEEP
            return FileAction.REVIEW
        
        # File-specific rules
        if path.suffix == '.py':
            if 'test' in path.name.lower():
                return FileAction.MERGE
            return FileAction.UPDATE if 'old_' in path.name else FileAction.KEEP
        
        if path.suffix in {'.tmp', '.bak', '.log'}:
            return FileAction.DELETE
        
        if path.suffix in {'.json', '.yaml', '.config'}:
            return FileAction.UPDATE
        
        return FileAction.REVIEW
    
    def _create_record(self, path: Path, action: FileAction) -> Dict:
        """Create a record for the file/directory"""
        if path.is_dir():
            size = sum(f.stat().st_size for f in path.glob('**/*') if f.is_file())
        else:
            size = path.stat().st_size
        
        return {
            'path': str(path),
            'action': action.name,
            'color': self.color_map[action],
            'size': size,
            'last_modified': path.stat().st_mtime,
            'notes': self._generate_notes(path, action)
        }
    
    def _generate_notes(self, path: Path, action: FileAction) -> str:
        """Generate notes based on the action"""
        if action == FileAction.DELETE:
            return "Scheduled for deletion - temporary or deprecated"
        elif action == FileAction.MERGE:
            return "Candidate for merging with other components"
        elif action == FileAction.UPDATE:
            return "Needs updating to current standards"
        elif action == FileAction.KEEP:
            return "Important file - preserve"
        else:
            return "Needs manual review"
    
    def _save_results_to_db(self, results: Dict):
        """Save scan results to the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for record in results.values():
                cursor.execute("""
                INSERT OR REPLACE INTO file_actions 
                (path, action, color, size, last_modified, notes)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    record['path'],
                    record['action'],
                    record['color'],
                    record['size'],
                    record['last_modified'],
                    record['notes']
                ))
            conn.commit()
    
    def generate_report(self, output_path: str = "file_actions_report.csv"):
        """Generate a CSV report of all actions"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM file_actions")
            records = cursor.fetchall()
        
        headers = ['Path', 'Action', 'Color', 'Size', 'Last Modified', 'Notes']
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(records)
        
        print(f"Report generated: {output_path}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python directory_scanner.py <path_to_scan>")
        sys.exit(1)
    
    target_path = sys.argv[1]
    if not Path(target_path).exists():
        print(f"Error: Path '{target_path}' does not exist")
        sys.exit(1)
    
    print(f"Scanning directory: {target_path}")
    scanner = DirectoryScanner(target_path)
    results = scanner.scan_directory()
    scanner.generate_report()
    
    print(f"Scan complete. {len(results)} items processed.")
    print("Color Key:")
    print("  GREEN (KEEP) - Important files to preserve")
    print("  BLUE (UPDATE) - Files needing updates")
    print("  PURPLE (MERGE) - Files to be merged")
    print("  RED (DELETE) - Files to be deleted")
    print("  PINK (REVIEW) - Needs manual review")