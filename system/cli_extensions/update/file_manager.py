# services/file_manager.py
import sqlite3
from pathlib import Path
from typing import Dict, List

class FileManager:
    def __init__(self, db_path: str = 'data/file_status.db'):
        self.db = sqlite3.connect(db_path)
        self._init_db()
    
    def _init_db(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS files (
            path TEXT PRIMARY KEY,
            status TEXT,
            metadata TEXT)''')
    
    def get_tree(self, root: str = None) -> List[Dict]:
        root = Path(root) if root else Path.cwd()
        return [
            self._file_info(item) 
            for item in root.iterdir()
        ]
    
    def _file_info(self, path: Path) -> Dict:
        status = self.db.execute(
            'SELECT status FROM files WHERE path = ?', 
            (str(path),)
        ).fetchone()
        
        return {
            'name': path.name,
            'path': str(path),
            'type': 'dir' if path.is_dir() else 'file',
            'status': status[0] if status else None
        }