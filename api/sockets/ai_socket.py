import json
from fastapi import WebSocket
from typing import Dict, Any
import logging
from engine import SlickLogicEngine
from memory import MemoryBank
from concurrent.futures import ThreadPoolExecutor

log = logging.getLogger(__name__)
executor = ThreadPoolExecutor(max_workers=4)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.engine = SlickLogicEngine(MemoryBank())

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        log.info(f"Client {client_id} connected")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            log.info(f"Client {client_id} disconnected")

    async def process_message(self, client_id: str, data: Dict[str, Any]):
        """Process message in background thread"""
        def _process():
            try:
                response = self.engine.process_query(
                    data["message"],
                    data.get("context", {})
                )
                return response
            except Exception as e:
                log.error(f"Processing error: {e}")
                return {"error": str(e)}

        future = executor.submit(_process)
        return future.result()

manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket):
    client_id = f"client_{id(websocket)}"
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                response = await manager.process_message(client_id, message)
                await websocket.send_json(response)
            except json.JSONDecodeError:
                await websocket.send_json({"error": "Invalid JSON"})
            except Exception as e:
                log.error(f"WebSocket error: {e}")
                await websocket.send_json({"error": str(e)})
                
    except WebSocketDisconnect:
        manager.disconnect(client_id)
