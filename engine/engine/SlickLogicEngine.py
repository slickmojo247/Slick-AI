import logging
from typing import Dict, Any
from memory.MemoryBank import MemoryBank
from cognitive.InterestEnhancer import InterestEnhancer

class SlickLogicEngine:
    MODES = ["balanced", "technical", "creative", "homer"]
    
    def __init__(self, memory: MemoryBank, mode: str = "balanced"):
        self.memory = memory
        self.mode = mode
        self.enhancer = InterestEnhancer()
        self.log = logging.getLogger(__name__)
        self.log.info(f"Engine initialized in {mode} mode")

    def process(self, query: str) -> Dict[str, Any]:
        """Full processing pipeline"""
        try:
            # 1. Context retrieval
            context = self.memory.get_context(query)
            
            # 2. Cognitive enhancement
            enhanced = self.enhancer.process(query, context)
            
            # 3. Mode-specific processing
            result = self._apply_mode(enhanced)
            
            # 4. Memory update
            self.memory.store(query, result)
            
            return {
                "status": "success",
                "query": query,
                "result": result,
                "mode": self.mode,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.log.error(f"Processing failed: {str(e)}")
            return {"status": "error", "message": str(e)}
            
    def _apply_mode(self, content: Dict) -> Dict:
        """Apply personality mode transformations"""
        if self.mode == "technical":
            content["precision"] = 0.9
            content["style"] = "concise"
        elif self.mode == "creative":
            content["creativity"] = 0.8
            content["style"] = "expressive"
        elif self.mode == "homer":
            content["humor"] = 0.95
            content["simplicity"] = 0.9
        else:  # balanced
            content["balance"] = 0.7
            
        return content
            
    def set_mode(self, new_mode: str):
        """Change processing mode"""
        if new_mode.lower() in self.MODES:
            self.mode = new_mode.lower()
            self.log.info(f"Changed mode to {self.mode}")
        else:
            raise ValueError(f"Invalid mode. Choose from: {self.MODES}")
