from abc import ABC, abstractmethod
import re

class Action(ABC):
    """Enhanced action base class with priority and context support"""
    priority: int = 0
    
    @property
    @abstractmethod
    def pattern(self) -> str:
        pass
    
    @abstractmethod
    async def execute(self, match: re.Match, context: dict) -> str:
        pass

class LightAction(Action):
    priority = 1
    
    @property
    def pattern(self) -> str:
        return r'turn (on|off) (?:the )?lights?'
    
    async def execute(self, match: re.Match, context: dict) -> str:
        return f"💡 Lights turned {match.group(1)}"

class GameAction(Action):
    @property
    def pattern(self) -> str:
        return r'trigger (\w+) event'
    
    async def execute(self, match: re.Match, context: dict) -> str:
        return f"🎮 Game event triggered: {match.group(1)}"