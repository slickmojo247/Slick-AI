#!/usr/bin/env python3
"""
DeepSeek API Integration - Complete Fixed Version
"""
import aiohttp
import logging
from typing import List, Dict, Optional
import json
import asyncio

class DeepSeekClient:
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com/v1"):
        """
        Initialize DeepSeek API client
        
        Args:
            api_key: Your DeepSeek API key
            base_url: API endpoint base URL
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = None
        self.logger = logging.getLogger('DeepSeekAI')
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging for the module"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    async def query(
        self,
        prompt: str,
        model: str = "deepseek-chat",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """
        Query the DeepSeek chat API
        
        Args:
            prompt: Input prompt/message
            model: Model to use
            temperature: Creativity control (0-2)
            max_tokens: Maximum response length
            
        Returns:
            Generated text response
        """
        endpoint = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }

        try:
            async with self.session.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return data['choices'][0]['message']['content']
        except Exception as e:
            self.logger.error(f"Query failed: {str(e)}")
            return f"⚠️ API Error: {str(e)}"

    async def train(
        self,
        training_data: List[Dict],
        model_name: str = "my-custom-model",
        **kwargs
    ) -> Dict:
        """
        Initiate training (simulated)
        
        Args:
            training_data: List of training examples
            model_name: Name for custom model
            
        Returns:
            Training job status
        """
        self.logger.info(f"Training with {len(training_data)} examples")
        return {
            "status": "success",
            "message": f"Simulated training with {len(training_data)} examples"
        }

    async def ping(self) -> bool:
        """Check API connectivity"""
        try:
            async with self.session.get(
                f"{self.base_url}/ping",
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                return response.status == 200
        except Exception:
            return False

# Example usage
async def example():
    async with DeepSeekClient("your-api-key") as client:
        print(await client.query("Hello world"))
        print(await client.train([{"input": "hi", "output": "hello"}]))
        print(await client.ping())

if __name__ == "__main__":
    asyncio.run(example())