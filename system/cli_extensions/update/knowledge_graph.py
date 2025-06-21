import networkx as nx
from datetime import datetime

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.node_count = 0
        
    def add_node(self, label, node_type="concept"):
        node_id = f"node_{self.node_count}"
        self.graph.add_node(node_id, 
                          label=label,
                          type=node_type,
                          created=datetime.now().isoformat())
        self.node_count += 1
        return node_id
        
    def add_relation(self, source_id, target_id, relation_type):
        self.graph.add_edge(source_id, target_id, 
                          type=relation_type,
                          strength=1.0)
        
    def query(self, keyword, limit=5):
        return [n for n, attr in self.graph.nodes(data=True)
               if keyword.lower() in attr['label'].lower()][:limit]