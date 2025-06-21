#!/usr/bin/env python3
"""
SLICK AI Core - Complete Working Version
"""
import logging
import openai
from typing import Dict
from dataclasses import dataclass
from ai_core.deepseek_integration import DeepSeekClient

@dataclass
class AIConfig:
    deepseek_api_key: str
    openai_api_key: str
    max_context_length: int = 4096

class SlickCore:
    def __init__(self, config: AIConfig):
        self.config = config
        self.logger = self._setup_logging()
        
        # Initialize AI services
        self.deepseek = DeepSeekClient(config.deepseek_api_key)
        openai.api_key = config.openai_api_key
        
        self.logger.info("SLICK Core initialized")

    def _setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger('SLICKCore')

    async def process(self, message: str) -> str:
        """Process message through AI pipeline"""
        try:
            # Get responses from both services
            deepseek_res = await self.deepseek.query(message)
            return f"🤖 AI Response:\n{deepseek_res}"
        except Exception as e:
            self.logger.error(f"Processing failed: {str(e)}")
            return "⚠️ Error processing request"

if __name__ == "__main__":
    # Test the core functionality
    import asyncio
    async def test():
        core = SlickCore(AIConfig(
            deepseek_api_key="test_key",
            openai_api_key="test_key"
        ))
        print(await core.process("Test message"))
    asyncio.run(test())