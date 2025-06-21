from typing import Dict, Any
import logging

class PersonalityEngine:
    MODES = {
        "balanced": {"creativity": 0.5, "precision": 0.5},
        "technical": {"creativity": 0.2, "precision": 0.9},
        "creative": {"creativity": 0.8, "precision": 0.3},
        "homer": {"creativity": 0.9, "precision": 0.1, "humor": 0.95}
    }

    def __init__(self, mode: str = "balanced"):
        self.log = logging.getLogger(__name__)
        self.mode = mode
        self.log.info(f"Personality Engine initialized in {mode} mode")

    def process(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process query according to personality mode"""
        mode_params = self.MODES[self.mode]
        
        if self.mode == "technical":
            return self._technical_process(query, context, mode_params)
        elif self.mode == "creative":
            return self._creative_process(query, context, mode_params)
        elif self.mode == "homer":
            return self._homer_process(query, context, mode_params)
        else:
            return self._balanced_process(query, context, mode_params)

    def _technical_process(self, query: str, context: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Technical precision-focused processing"""
        return {
            "content": f"Technical analysis of: {query}",
            "style": "structured",
            "confidence": params["precision"],
            "sections": [
                {"title": "Definition", "content": f"Explanation of {query}"},
                {"title": "Implementation", "content": "Code example here"},
                {"title": "Best Practices", "content": "Recommended approaches"}
            ]
        }

    def _creative_process(self, query: str, context: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Creative idea generation"""
        return {
            "content": f"Creative exploration of: {query}",
            "style": "expressive",
            "confidence": params["creativity"],
            "ideas": [
                f"Alternative perspective: {query} as a metaphor",
                f"Artistic interpretation: {query} in visual form",
                f"Narrative approach: Story about {query}"
            ]
        }

    def _homer_process(self, query: str, context: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Homer personality processing"""
        homerisms = ["D'oh!", "Mmm...", "Woo-hoo!", "Why you little..."]
        import random
        return {
            "content": f"{random.choice(homerisms)} {query}",
            "style": "humorous",
            "confidence": params["humor"],
            "simplified": f"Basically, {query.lower()}"
        }

    def _balanced_process(self, query: str, context: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Balanced processing"""
        return {
            "content": f"Comprehensive response to: {query}",
            "style": "neutral",
            "confidence": (params["creativity"] + params["precision"]) / 2,
            "points": [
                f"Key fact about {query}",
                f"Practical application of {query}",
                f"Considerations regarding {query}"
            ]
        }

    def set_mode(self, new_mode: str):
        """Change processing mode"""
        if new_mode.lower() in self.MODES:
            self.mode = new_mode.lower()
            self.log.info(f"Changed to {self.mode} mode")
            return True
        raise ValueError(f"Invalid mode. Choose from: {list(self.MODES.keys())}")
