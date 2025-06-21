import os
import httpx
from typing import Optional, Literal

AIModel = Literal['gpt-4', 'deepseek-coder', 'hybrid']

class AIConnector:
    def __init__(self):
        self.clients = {
            'openai': AsyncOpenAI(api_key=os.getenv('OPENAI_KEY')),
            'deepseek': httpx.AsyncClient(
                base_url='https://api.deepseek.com/v1',
                headers={'Authorization': f"Bearer {os.getenv('DEEPSEEK_KEY')}"}
            )
        }
    
    async def generate(self, prompt: str, context: dict, model: AIModel = 'hybrid') -> str:
        """Smart routing between AI providers"""
        if model == 'hybrid':
            model = 'deepseek-coder' if self._is_code_request(prompt) else 'gpt-4'
        
        if 'deepseek' in model:
            return await self._deepseek_request(prompt, model)
        return await self._openai_request(prompt, model)
    
    def _is_code_request(self, prompt: str) -> bool:
        code_keywords = {'code', 'debug', 'syntax', 'algorithm'}
        return any(kw in prompt.lower() for kw in code_keywords)
    
    async def _openai_request(self, prompt: str, model: str) -> str:
        response = await self.clients['openai'].chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response.choices[0].message.content
    
    async def _deepseek_request(self, prompt: str, model: str) -> str:
        response = await self.clients['deepseek'].post(
            '/chat/completions',
            json={'model': model, 'messages': [{'role': 'user', 'content': prompt}]}
        )
        return response.json()['choices'][0]['message']['content']