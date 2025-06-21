import json
from pathlib import Path
from typing import Dict, Any

class AIPreferences:
    def __init__(self, config_path: str = "config/ai_preferences.json"):
        self.config_path = Path(config_path)
        self.preferences = self._load_preferences()

    def _load_preferences(self) -> Dict[str, Any]:
        """Load preferences from JSON file"""
        try:
            with open(self.config_path) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return self._create_default_preferences()

    def _create_default_preferences(self) -> Dict[str, Any]:
        """Create default preferences if none exist"""
        defaults = {
            "default_mode": "balanced",
            "provider_weights": {
                "openai": 0.7,
                "deepseek": 0.3
            },
            "personality_settings": {
                "homer": {
                    "humor_level": 0.9,
                    "simplicity": 0.8
                }
            }
        }
        self.config_path.parent.mkdir(exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(defaults, f, indent=2)
        return defaults

    def get_mode_settings(self, mode: str) -> Dict[str, Any]:
        """Get settings for specific mode"""
        return self.preferences.get('personality_settings', {}).get(mode, {})
