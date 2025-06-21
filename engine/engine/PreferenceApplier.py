import logging
from typing import Dict, Any

class PreferenceApplier:
    """Handles response style formatting based on preferences"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.style_profiles = {
            "balanced": self._apply_balanced_style,
            "technical": self._apply_technical_style,
            "creative": self._apply_creative_style,
            "homer": self._apply_homer_style
        }
        
    def apply_preferences(self, query: str, mode: str = "balanced", context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Apply style preferences to the response"""
        processor = self.style_profiles.get(mode.lower(), self._apply_balanced_style)
        return processor(query, context)
        
    def _apply_balanced_style(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Default balanced response style"""
        return {
            "original_query": query,
            "processed_query": query,
            "style": "balanced",
            "enhancements": []
        }
        
    def _apply_technical_style(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Technical precision-focused style"""
        return {
            "original_query": query,
            "processed_query": f"[Technical Analysis] {query}",
            "style": "technical",
            "enhancements": ["precision_boost"]
        }
        
    def _apply_creative_style(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Creative idea generation style"""
        return {
            "original_query": query,
            "processed_query": f"[Creative Exploration] {query}",
            "style": "creative",
            "enhancements": ["creativity_boost"]
        }
        
    def _apply_homer_style(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Homer personality mode"""
        homerisms = ["D'oh!", "Mmm...", "Woo-hoo!", "Why you little..."]
        import random
        return {
            "original_query": query,
            "processed_query": f"{random.choice(homerisms)} {query}",
            "style": "homer",
            "enhancements": ["humor_boost", "simplification"]
        }