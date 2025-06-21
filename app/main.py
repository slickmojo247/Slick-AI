from fastapi import FastAPI
from api.websocket import router as ws_router
from backend.ai_route import router as ai_router

app = FastAPI(
    title="Slick AI API",
    description="WebSocket and API endpoints for Slick AI System",
    version="1.2.0"
)

app.include_router(ws_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Slick AI System Online"}