from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.routing import APIRouter
import json
from engine.slick_logic import SlickLogicEngine
from ai_core.orchestrator import AIOrchestrator

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections = []
        self.logic_engine = SlickLogicEngine()
        self.ai_orchestrator = AIOrchestrator()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def process_message(self, message: str, websocket: WebSocket):
        try:
            data = json.loads(message)
            
            # Process through logic engine first
            processed = self.logic_engine.pre_process(data['message'])
            
            # Get AI response
            ai_response = await self.ai_orchestrator.route_query(processed)
            
            # Post-process response
            final_response = self.logic_engine.post_process(ai_response)
            
            await websocket.send_json({
                "type": "ai_response",
                "content": final_response
            })
            
        except Exception as e:
            await websocket.send_json({
                "type": "error",
                "content": str(e)
            })

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.process_message(data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)