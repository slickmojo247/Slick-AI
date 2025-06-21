# vscode_integration/server.py
import websockets

class VSCodeExtension:
    def __init__(self):
        self.connections = set()
        
    async def register(self, websocket):
        self.connections.add(websocket)
        
    async def broadcast(self, message):
        for connection in self.connections:
            await connection.send(message)