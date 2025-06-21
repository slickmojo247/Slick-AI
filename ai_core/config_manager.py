import yaml
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv
import os

class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_config()
        return cls._instance

    def _init_config(self):
        """Load configuration from multiple sources"""
        load_dotenv()  # Load .env file
        
        self.config = {
            "providers": {},
            "blending": {},
            "logging": {}
        }
        
        # Load from YAML config
        config_path = Path("config/ai_core.yaml")
        if config_path.exists():
            with open(config_path) as f:
                self.config.update(yaml.safe_load(f) or {})
        
        # Environment variables override
        self._load_env_vars()

    def _load_env_vars(self):
        """Load environment variables"""
        self.config["providers"]["openai_key"] = os.getenv("OPENAI_KEY")
        self.config["providers"]["deepseek_key"] = os.getenv("DEEPSEEK_KEY")
        self.config["logging"]["level"] = os.getenv("LOG_LEVEL", "INFO")

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value using dot notation"""
        keys = key.split('.')
        val = self.config
        try:
            for k in keys:
                val = val[k]
            return val
        except KeyError:
            return default

    def hot_reload(self):
        """Reload configuration"""
        self._init_config()
