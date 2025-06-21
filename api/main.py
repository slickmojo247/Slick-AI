from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import Dict, Any
from engine import SlickLogicEngine
from memory import MemoryBank

class APIServer:
    def __init__(self):
        self.app = FastAPI(
            title="Slick AI API",
            version="2.1.0",
            description="API for Slick AI System"
        )
        self._setup_middleware()
        self._setup_routes()
        self.log = logging.getLogger(__name__)
        
        # Initialize core systems
        self.memory = MemoryBank()
        self.engine = SlickLogicEngine(self.memory)
        
        self.log.info("API Server initialized")

    def _setup_middleware(self):
        """Configure API middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _setup_routes(self):
        """Register API routes"""
        from .endpoints import chat, system
        from .sockets import ai_socket
        
        self.app.include_router(chat.router, prefix="/api/v1")
        self.app.include_router(system.router, prefix="/api/v1")
        self.app.websocket("/ws/ai")(ai_socket.websocket_endpoint)

    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the API server"""
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)

app = APIServer().app

if __name__ == "__main__":
    APIServer().run()
