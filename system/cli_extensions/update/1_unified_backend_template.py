"""Merges: 
- sync_server.py 
- secure_sync.py 
- key_vault.py
- web_server.py
"""
import websockets
from cryptography.fernet import Fernet
import uvicorn
from fastapi import FastAPI

class SecureVSCodeSync:
    def __init__(self):
        self.cipher = Fernet(os.getenv('ENCRYPTION_KEY'))
        self.connections = set()
        
    async def handle_connection(self, websocket):
        """Combined sync logic"""
        self.connections.add(websocket)
        try:
            async for message in websocket:
                decrypted = self.cipher.decrypt(message)
                await self.broadcast(decrypted)
        finally:
            self.connections.remove(websocket)

class WebService(FastAPI):
    """Merged web servers"""
    def __init__(self):
        super().__init__()
        self.vsc_sync = SecureVSCodeSync()
        self.add_api_routes()
        
    def add_api_routes(self):
        @self.get("/api/commands")
        async def get_commands():
            return {"status": "active"}  # Your full endpoint logic here

if __name__ == "__main__":
    service = WebService()
    uvicorn.run(service, port=8000)