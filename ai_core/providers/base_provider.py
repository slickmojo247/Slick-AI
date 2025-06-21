import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseProvider(ABC):
    def __init__(self, provider_name: str):
        self.log = logging.getLogger(f"{provider_name.upper()}Provider")
        self.provider_name = provider_name
        self.log.info(f"Initialized {provider_name} provider")

    @abstractmethod
    def process(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing method"""
        pass

    def validate_response(self, response: Dict[str, Any]) -> bool:
        """Validate API response structure"""
        required = ['content', 'model']
        return all(key in response for key in required)

    def log_usage(self, response: Dict[str, Any]):
        """Log token usage"""
        tokens = response.get('usage', {}).get('total_tokens', 0)
        self.log.debug(f"Used {tokens} tokens")

    def _build_context_str(self, context: Dict[str, Any]) -> str:
        """Serialize context for prompts"""
        return str(context)[:500]  # Limit context size
