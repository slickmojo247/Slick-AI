from pydantic import BaseModel
from typing import Optional, Dict, Any

class ChatRequest(BaseModel):
    message: str
    mode: Optional[str] = "balanced"
    context: Optional[Dict[str, Any]] = None

class FeedbackRequest(BaseModel):
    query: str
    response: str
    rating: int
    comments: Optional[str] = None

class SystemModeRequest(BaseModel):
    mode: str
