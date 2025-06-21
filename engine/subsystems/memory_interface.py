from typing import Dict, Any, List
import logging

class MemoryInterface:
    def __init__(self, memory_system):
        self.log = logging.getLogger(__name__)
        self.memory = memory_system
        self.log.info("Memory Interface initialized")

    def store_interaction(self, query: str, response: Dict[str, Any], context: Dict[str, Any]):
        """Store a complete interaction in memory"""
        interaction = {
            "query": query,
            "response": response,
            "context": context,
            "timestamp": self._get_timestamp()
        }
        self.memory.store(interaction)
        self.log.debug(f"Stored interaction: {query[:50]}...")

    def get_context(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """Retrieve relevant context for a query"""
        return self.memory.retrieve(query, max_results)

    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()
