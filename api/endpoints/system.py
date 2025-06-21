from fastapi import APIRouter
from pydantic import BaseModel
import logging
from engine import SlickLogicEngine

router = APIRouter()
log = logging.getLogger(__name__)

class SystemMode(BaseModel):
    mode: str

@router.post("/system/mode")
async def set_mode(request: SystemMode):
    """Change system personality mode"""
    try:
        engine = SlickLogicEngine()  # Would be dependency injected
        engine.set_personality_mode(request.mode)
        return {"status": "success", "mode": request.mode}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        log.error(f"Mode change error: {e}")
        raise HTTPException(500, detail="Internal server error")

@router.get("/system/status")
async def get_status():
    """Get system health status"""
    return {
        "status": "operational",
        "components": ["engine", "memory", "api"]
    }
