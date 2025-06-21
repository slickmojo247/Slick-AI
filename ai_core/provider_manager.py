import importlib
from typing import Dict, Type
from .providers.base_provider import BaseProvider

class ProviderManager:
    _providers: Dict[str, Type[BaseProvider]] = {}

    @classmethod
    def register_provider(cls, name: str):
        """Decorator to register providers"""
        def decorator(provider_class: Type[BaseProvider]):
            cls._providers[name.lower()] = provider_class
            return provider_class
        return decorator

    @classmethod
    def get_provider(cls, name: str, config: Dict) -> BaseProvider:
        """Dynamically load provider"""
        name = name.lower()
        if name not in cls._providers:
            self._load_provider_module(name)
        
        if name not in cls._providers:
            raise ValueError(f"Unknown provider: {name}")
            
        return cls._providers[name](config)

    @classmethod
    def _load_provider_module(cls, name: str):
        """Attempt to load provider module"""
        try:
            module = importlib.import_module(f"ai_core.providers.{name}_provider")
            # Module auto-registers via decorator
        except ImportError:
            pass
