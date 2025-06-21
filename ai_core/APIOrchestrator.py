import logging
from typing import Dict, Any, Optional
from .providers import OpenAIProvider, DeepSeekProvider
from .utils.response_blender import ResponseBlender
from .config_manager import ConfigManager

class APIOrchestrator:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.config = ConfigManager()
        self._init_providers()
        self.blender = ResponseBlender()
        self.log.info("API Orchestrator initialized")

    def _init_providers(self):
        """Initialize providers from config"""
        provider_config = self.config.get("providers", {})
        self.openai = OpenAIProvider(provider_config.get("openai", {}))
        self.deepseek = DeepSeekProvider(provider_config.get("deepseek", {}))

    def route_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Route query to appropriate providers and blend responses"""
        try:
            context = context or {}
            # Determine primary provider based on query type
            primary, secondary = self._select_providers(query)
            
            # Get responses
            primary_resp = primary.process(query, context)
            secondary_resp = secondary.process(query, context)

            # Blend responses
            blended = self.blender.blend(
                responses=[primary_resp, secondary_resp],
                mode=context.get('mode', 'balanced')
            )

            return {
                "status": "success",
                "query": query,
                "response": blended,
                "providers": {
                    "primary": primary.provider_name,
                    "secondary": secondary.provider_name
                }
            }
        except Exception as e:
            self.log.error(f"Routing failed: {e}")
            return {"status": "error", "message": str(e)}

    def _select_providers(self, query: str):
        """Select providers based on query content"""
        tech_keywords = ['code', 'algorithm', 'debug', 'function', 'class']
        if any(keyword in query.lower() for keyword in tech_keywords):
            return self.deepseek, self.openai
        return self.openai, self.deepseek
