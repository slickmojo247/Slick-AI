# core/application.py - Unified entry point
from interfaces.web.server import WebServer
from interfaces.telegram.bot import TelegramBot
from services.ai.knowledge import KnowledgeCore
from fastapi import FastAPI, Security
from .security import APIKeyHeader
from .routing import router as core_router
from config import Config

config = Config()
app = FastAPI()
auth = APIKeyHeader(name="X-API-KEY")

app.include_router(core_router)

@app.on_event("startup")
async def startup_event():
    if not config.verify():
        raise RuntimeError("Missing required configuration")

class SlickAI:
    def __init__(self):
        self.knowledge = KnowledgeCore()
        self.web = WebServer(self)
        self.telegram = TelegramBot(self)
        
    async def start(self):
        await asyncio.gather(
            self.web.start(),
            self.telegram.start()
        )    