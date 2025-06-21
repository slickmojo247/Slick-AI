from fastapi import FastAPI
import uvicorn
import logging

logger = logging.getLogger('WebServer')

class WebServer:
    def __init__(self):
        self.app = FastAPI()
        self.server = None
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.get("/")
        async def root():
            return {"status": "SLICK AI is running"}
    
    async def serve_async(self):
        """Run the server in async mode"""
        config = uvicorn.Config(
            app=self.app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
        self.server = uvicorn.Server(config)
        await self.server.serve()
    
    async def stop(self):
        """Stop the server gracefully"""
        if self.server:
            logger.info("Stopping web server")
            self.server.should_exit = True
            await self.server.shutdown()