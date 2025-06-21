import datetime
from dateutil.parser import parse

class MemoryBank:
    def __init__(self):
        self.long_term = {}
        self.decay_alpha = 0.15
        self.decay_beta = 0.12
        
    def add_memory(self, event, importance=0.7):
        mem_id = f"mem_{len(self.long_term)+1}"
        self.long_term[mem_id] = {
            'content': event,
            'timestamp': datetime.now().isoformat(),
            'importance': importance,
            'decayed': importance
        }
        return mem_id
        
    def apply_decay(self, aggressive=False):
        for mem_id, mem in list(self.long_term.items()):
            # Decay calculation logic here
            if mem['decayed'] < 0.05:
                del self.long_term[mem_id]