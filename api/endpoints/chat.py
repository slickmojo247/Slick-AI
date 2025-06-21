from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
from engine import SlickLogicEngine
from memory import MemoryBank

router = APIRouter()
log = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str
    mode: Optional[str] = "balanced"
    context: Optional[dict] = None

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Main chat API endpoint"""
    try:
        # Get engine instance (would be dependency injected in real app)
        engine = SlickLogicEngine(MemoryBank())
        engine.set_personality_mode(request.mode)
        
        response = engine.process_query(
            request.message,
            request.context or {}
        )
        
        if response["status"] == "error":
            raise HTTPException(500, detail=response["message"])
            
        return {
            "response": response["response"],
            "context": response["context"]
        }
        
    except Exception as e:
        log.error(f"Chat error: {e}")
        raise HTTPException(500, detail=str(e))
