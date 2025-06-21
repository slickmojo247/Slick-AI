# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

class APIConfig:
    OPENAI_KEY = os.getenv("OPENAI_API_KEY")
    DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    @classmethod
    def verify_keys(cls):
        """Verify all API keys are present"""
        keys = [cls.OPENAI_KEY, cls.DEEPSEEK_KEY, cls.TELEGRAM_TOKEN]
        return all(keys)

class Settings:
    MEMORY_DECAY_RATES = {
        'default': {'alpha': 0.15, 'beta': 0.12},
        'aggressive': {'alpha': 0.3, 'beta': 0.2}
    }
    
    EXPORT_PATHS = {
        'memory': './exports/memory',
        'knowledge': './exports/knowledge'
    }