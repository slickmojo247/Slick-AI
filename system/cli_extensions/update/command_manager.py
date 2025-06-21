# services/command_manager.py
from typing import Dict, List

class CommandManager:
    def __init__(self):
        self.commands = {
            "CURE": {
                "description": "Restore player health to maximum",
                "status": False,
                "dependencies": ["requests", "boto3"],
                "color": "#FF6B6B",
                "icon": "fa-heartbeat"
            },
            "LOOK": {
                "description": "Enable cosmic vision",
                "status": False,
                "dependencies": ["requests", "pusher"],
                "color": "#4ECDC4",
                "icon": "fa-eye"
            }
        }
        
    def get_command(self, name: str) -> Dict:
        return self.commands.get(name)
        
    def get_all_commands(self) -> Dict:
        return self.commands
        
    def toggle_command(self, name: str) -> bool:
        if name not in self.commands:
            raise ValueError(f"Command '{name}' not found")
        self.commands[name]["status"] = not self.commands[name]["status"]
        return self.commands[name]["status"]
        
    def add_command(self, name: str, description: str, dependencies: List[str] = None) -> None:
        if name in self.commands:
            raise ValueError(f"Command '{name}' already exists")
        self.commands[name] = {
            "description": description,
            "status": False,
            "dependencies": dependencies or [],
            "color": "#FFFFFF",
            "icon": "fa-cog"
        }
        
    def remove_command(self, name: str) -> None:
        if name not in self.commands:
            raise ValueError(f"Command '{name}' not found")
        del self.commands[name]