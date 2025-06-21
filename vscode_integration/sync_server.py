import websockets
from cryptography.fernet import Fernet

class VSCodeSync:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.connections = set()

    async def handle_connection(self, websocket):
        self.connections.add(websocket)
        try:
            async for message in websocket:
                decrypted = Fernet(self.key).decrypt(message)
                await self._broadcast(decrypted)
        finally:
            self.connections.remove(websocket)

    async def _broadcast(self, message):
        for conn in self.connections:
            await conn.send(message)
