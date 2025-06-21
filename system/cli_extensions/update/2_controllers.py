from typing import Dict, List
from .action import Action
from ..connectors.ai import AIConnector
from ..connectors.messaging import TelegramConnector

class SlickController:
    def __init__(self):
        self.actions: List[Action] = []
        self.ai = AIConnector()
        self.messaging = TelegramConnector()
    
    async def handle_request(self, input_str: str, context: Dict = None) -> str:
        """Process input through action system or AI"""
        context = context or {}
        
        # Try actions first
        for action in sorted(self.actions, key=lambda a: a.priority, reverse=True):
            if match := re.search(action.pattern, input_str, re.IGNORECASE):
                return await action.execute(match, context)
        
        # Fallback to AI
        return await self.ai.generate(input_str, context)