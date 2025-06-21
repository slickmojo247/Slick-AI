import logging
from typing import Dict, Any, Optional
from datetime import datetime
from .subsystems import PersonalityEngine, MemoryInterface, LearningEngine
from .utils import ContextBuilder, PerformanceMonitor

class SlickLogicEngine:
    def __init__(self, memory, config: Optional[Dict[str, Any]] = None):
        self.log = logging.getLogger(__name__)
        self.memory = memory
        self.config = config or {}
        self._init_subsystems()
        self.log.info("Enhanced Logic Engine initialized")

    def _init_subsystems(self):
        """Initialize all engine subsystems"""
        self.personality = PersonalityEngine(
            mode=self.config.get("personality_mode", "balanced")
        )
        self.memory_interface = MemoryInterface(self.memory)
        self.learning_engine = LearningEngine()
        self.context_builder = ContextBuilder()
        self.monitor = PerformanceMonitor()

    @PerformanceMonitor().track
    def process_query(self, query: str, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Enhanced processing pipeline with monitoring"""
        try:
            # Track mode usage
            self.monitor.record_mode_usage(self.personality.mode)
            
            # Build context
            context = self.context_builder.build(
                query=query,
                memory=self.memory_interface,
                user_context=user_context or {}
            )
            
            # Process with personality
            processed = self.personality.process(query, context)
            
            # Store interaction
            self.memory_interface.store_interaction(
                query=query,
                response=processed,
                context=context
            )
            
            return {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "response": processed,
                "context": context
            }
            
        except Exception as e:
            self.log.error(f"Processing failed: {e}")
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def set_personality_mode(self, mode: str):
        """Change personality mode with validation"""
        self.personality.set_mode(mode)
        self.log.info(f"Personality mode changed to {mode}")

    def get_performance_report(self) -> Dict[str, Any]:
        """Get system performance metrics"""
        return self.monitor.get_report()

    def provide_feedback(self, feedback: Dict[str, Any]):
        """Learn from user feedback"""
        self.learning_engine.process_feedback(feedback)
