import logging
from typing import Dict, Any
from ..interfaces.cli import CommandRegistry
from ..services.ai.connector import AIConnector
from ..system.memory import MemoryManager

class AICore:
    def __init__(self):
        self.connector = AIConnector()
        self.memory = MemoryManager()
        self.command_registry = CommandRegistry(self)  # Inject core into commands
        
        # Initialize subsystems
        self._init_cli_commands()
        
    def _init_cli_commands(self):
        """Register core commands"""
        from ..cli.commands.system import register_system_commands
        from ..cli.commands.ai import register_ai_commands
        
        register_system_commands(self.command_registry)
        register_ai_commands(self.command_registry)
        
    def execute_command(self, command: str, args: Dict[str, Any]):
        """Central command execution"""
        try:
            return self.command_registry.execute(command, args)
        except Exception as e:
            logging.error(f"Command failed: {str(e)}")
            raise