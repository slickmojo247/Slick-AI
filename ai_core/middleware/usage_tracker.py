import time
from datetime import datetime
from typing import Callable, Dict, Any
import sqlite3
from pathlib import Path

class UsageTracker:
    def __init__(self, db_path: str = "data/usage.db"):
        self.db_path = Path(db_path)
        self._init_db()

    def __call__(self, func: Callable) -> Callable:
        """Decorator to track API usage"""
        def wrapped(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            self.log_usage(
                function=func.__name__,
                duration=end_time - start_time,
                metadata={
                    "args": str(args)[:100],
                    "kwargs": str(kwargs)[:100],
                    "success": "error" not in result
                }
            )
            return result
        return wrapped

    def _init_db(self):
        """Initialize usage database"""
        self.db_path.parent.mkdir(exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS api_usage (
                    id INTEGER PRIMARY KEY,
                    timestamp DATETIME,
                    function TEXT,
                    duration REAL,
                    metadata TEXT
                )
            """)

    def log_usage(self, function: str, duration: float, metadata: Dict):
        """Log usage to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO api_usage (timestamp, function, duration, metadata) VALUES (?, ?, ?, ?)",
                (datetime.now(), function, duration, str(metadata))
            )
