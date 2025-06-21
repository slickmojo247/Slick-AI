# config.py
import os

class Config:
    def __init__(self):
        self.settings = {
            'OPENAI_API_KEY': os.getenv("OPENAI_API_KEY"),
            'DEEPSEEK_API_KEY': os.getenv("DEEPSEEK_API_KEY"),
            'TELEGRAM_TOKEN': os.getenv("TELEGRAM_BOT_TOKEN"),
            'DEBUG': os.getenv("SLICK_DEBUG", "True") == "True"
        }
        
    def verify(self):
        required = ['OPENAI_API_KEY', 'DEEPSEEK_API_KEY']
        return all(self.settings[key] for key in required)