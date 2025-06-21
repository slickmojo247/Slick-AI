# knowledge_integration/think_session_processor.py
import glob
import json
from pathlib import Path
from ai_core.learning_engine.knowledge_graph import KnowledgeGraph

class ThinkSessionIntegrator:
    def __init__(self, sessions_path: str = "think_sessions/"):
        self.sessions_path = Path(sessions_path)
        self.sessions_path.mkdir(exist_ok=True)
        
    def load_all_sessions(self) -> dict:
        """Load all think sessions into a structured format"""
        sessions = {}
        for file in glob.glob(str(self.sessions_path / "Think_session*.txt")):
            session_id = Path(file).stem
            with open(file, 'r') as f:
                content = f.read()
                sessions[session_id] = self._parse_session(content)
        return sessions

    def _parse_session(self, content: str) -> dict:
        """Convert raw session text to structured knowledge"""
        # Custom parsing logic based on your session format
        sections = content.split("\n\n")
        return {
            "metadata": self._extract_metadata(sections[0]),
            "core_ideas": sections[1].split("\n- ")[1:],
            "action_items": sections[2].split("\n* ")[1:],
            "connections": self._extract_connections(sections[3])
        }

    def integrate_with_knowledge_graph(self, kg: KnowledgeGraph):
        """Connect sessions to Slick's knowledge base"""
        for session_id, content in self.load_all_sessions().items():
            kg.add_node(session_id, "think_session", content["metadata"])
            
            for idea in content["core_ideas"]:
                kg.add_node(idea, "concept")
                kg.add_edge(session_id, idea, "contains")
                
            for item in content["action_items"]:
                kg.add_node(item, "action")
                kg.add_edge(session_id, item, "requires")
                
            for connection in content["connections"]:
                kg.add_edge(session_id, connection["target"], connection["type"])