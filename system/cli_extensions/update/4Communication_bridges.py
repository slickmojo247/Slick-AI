# Merges: telegram.py, vscode.py, core.py
from telegram.ext import Application

class CommsManager:
    def __init__(self):
        self.connections = {}  # websockets
        self.tg_bot = Application.builder().token(TELEGRAM_TOKEN).build()
        
    async def broadcast(self, msg_type, data):
        """Send to all connected clients"""
        for ws in self.connections.values():
            await ws.send_json({"type": msg_type, "data": data})
    
    def setup_telegram(self):
        self.tg_bot.add_handler(MessageHandler(
            filters.TEXT, self.handle_telegram))
        
    async def handle_telegram(self, update, ctx):
        if "```" in update.message.text:  # Code block
            await self.broadcast("vscode_code", extract_code(update.message.text))