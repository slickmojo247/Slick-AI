# Merges: files.py, M.py, Master_Loader.py
import sqlite3, zipfile, json

class FileManager:
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("CREATE TABLE files(path TEXT PRIMARY KEY, content TEXT)")
    
    def sync(self, path: str, content: str):
        """VSCode/web sync with conflict detection"""
        curr = self.conn.execute("SELECT content FROM files WHERE path=?", (path,)).fetchone()
        if curr and curr[0] != content:
            raise ConflictError(path, curr[0], content)
        self.conn.execute("REPLACE INTO files VALUES(?,?)", (path, content))

class Memory:
    def __init__(self):
        self.data = {}
    
    def save(self, key, value):
        with open("memory.json", "w") as f:
            json.dump({**self.data, key: value}, f)