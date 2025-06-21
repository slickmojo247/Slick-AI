import pickle
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

class MemoryBank:
    def __init__(self, storage_path: str = "data/memory.db"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(exist_ok=True)
        self.entries: List[Dict] = []
        self._load()

    def store(self, query: str, result: Dict) -> str:
        """Store interaction with timestamp"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "result": result,
            "access_count": 0
        }
        self.entries.append(entry)
        self._save()
        return entry["timestamp"]

    def get_context(self, query: str, limit: int = 3) -> List[Dict]:
        """Retrieve relevant context for query"""
        relevant = sorted(
            [e for e in self.entries if self._is_relevant(e, query)],
            key=lambda x: x["access_count"],
            reverse=True
        )[:limit]
        
        # Update access counts
        for entry in relevant:
            entry["access_count"] += 1
            
        return relevant

    def _is_relevant(self, entry: Dict, query: str) -> bool:
        """Basic relevance detection"""
        q_words = set(query.lower().split())
        e_words = set(entry["query"].lower().split())
        return len(q_words & e_words) > 0

    def _load(self):
        """Load memory from disk"""
        try:
            if self.storage_path.exists():
                with open(self.storage_path, "rb") as f:
                    self.entries = pickle.load(f)
        except Exception as e:
            print(f"Memory load error: {e}")

    def _save(self):
        """Atomic memory save"""
        if self.storage_path == Path(":memory:"):
            return
            
        temp_path = self.storage_path.with_suffix(".tmp")
        try:
            with open(temp_path, "wb") as f:
                pickle.dump(self.entries, f)
            temp_path.replace(self.storage_path)
        except Exception as e:
            print(f"Memory save error: {e}")
