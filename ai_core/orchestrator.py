import openai
import deepseek
from memory import MemoryBank

class AIOrchestrator:
    def __init__(self):
        self.memory = MemoryBank()
        self.router = {
            'creative': 'openai',
            'technical': 'deepseek',
            'hybrid': 'auto'
        }
    
    def route_query(self, query):
        context = self.memory.get_context(query)
        if 'code' in context.tags:
            return self.router['technical']
        return self.router['hybrid']
