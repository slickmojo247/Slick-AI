import asyncio
from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum
from fastapi import FastAPI
from utils.memory_reset import MemoryResetManager
from data_exporter import SystemDataExporter

class SlickController:
    def __init__(self):
        self.memory_bank = MemoryBank()
        self.reset_manager = MemoryResetManager(self.memory_bank)
        self.exporter = SystemDataExporter()
        self.version = "2.1.0"
        
    async def reset_memory(self, reset_type="soft"):
        result = await self.reset_manager.handle_reset(reset_type)
        self.exporter.log_reset(result)
        return result
        
    def export_data(self, scope="all"):
        return self.exporter.generate_report(scope)

    def full_reset(self):
        self.memory_bank.clear()
        self.reset_manager.cleanup_old_saves()

# Initialize FastAPI app
app = FastAPI()

class AIService(Enum):
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    HYBRID = "hybrid"

@dataclass
class UserRequest:
    source: str  # 'vscode', 'web', 'telegram'
    input: str
    context: Dict = None
    preferred_ai: AIService = AIService.HYBRID

# Define the main controller class
class SlickController:
    def __init__(self):
        self.ai_router = AIRouter()
        self.knowledge_base = KnowledgeBase()
        self.version_control = VersionControlSystem()
        self.testing_suite = TestingFramework()

        # Initialize interfaces
        self.vscode_interface = VSCodeInterface(self)
        self.web_interface = WebInterface(self)
        self.telegram_interface = TelegramInterface(self)

    async def handle_request(self, request: UserRequest) -> Dict:
        """Main request handling pipeline"""
        # 1. Apply think files context
        enhanced_input = self._apply_think_context(request.input)
        
        # 2. Route to appropriate AI service
        ai_service = self._select_ai_service(enhanced_input, request.preferred_ai)
        response = await self.ai_router.route(
            prompt=enhanced_input,
            service=ai_service,
            context=request.context
        )
        
        # 3. Store in knowledge base
        await self.knowledge_base.log_interaction(
            input=request.input,
            response=response,
            source=request.source
        )
        
        # 4. Return formatted output
        return self._format_response(response, request.source)

    def _apply_think_context(self, input_text: str) -> str:
        """Enhance input with think files knowledge"""
        return f"Context-enhanced: {input_text}"

    def _select_ai_service(self, text: str, preferred: AIService) -> AIService:
        """Smart routing between AI providers"""
        if preferred != AIService.HYBRID:
            return preferred
            
        # Hybrid routing logic
        code_keywords = {'function', 'class', 'def', 'import', 'print'}
        if any(kw in text.lower() for kw in code_keywords):
            return AIService.DEEPSEEK
        return AIService.OPENAI

    def _format_response(self, response: str, source: str) -> Dict:
        """Format response for different interfaces"""
        if source == 'vscode':
            return {'vscode_format': response}
        elif source == 'telegram':
            return {'telegram_format': f"🤖 {response}"}
        else:  # web
            return {'html': f"<div class='ai-response'>{response}</div>"}

# FastAPI routes

@app.post("/api/query")
async def handle_query(request: UserRequest):
    """API endpoint to handle requests through SlickController."""
    # Process the request through the SlickController
    response = await slick_controller.handle_request(request)
    return response
