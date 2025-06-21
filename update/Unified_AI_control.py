"""
SLICK AI - Unified Interface System
Combines:
- Web dashboard (FastAPI/Flask)
- Telegram bot interface
- Voice interface
- CLI interface
- Proxy configuration
"""

import asyncio
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn
import speech_recognition as sr
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging
from typing import Optional

# ========================
# CORE INTERFACE CLASSES
# ========================

class InterfaceManager:
    """Central manager for all interface types"""
    def __init__(self, core):
        self.core = core
        self.logger = logging.getLogger('InterfaceManager')
        
        # Initialize all interfaces
        self.web = WebInterface(self.core)
        self.telegram = TelegramInterface(self.core)
        self.voice = VoiceInterface()
        self.cli = CLIInterface(self.core)
        
        # State tracking
        self.active_interfaces = set()

    async def start_interface(self, interface_name: str):
        """Start a specific interface"""
        try:
            if interface_name == "web":
                self.web.run()
                self.active_interfaces.add("web")
            elif interface_name == "telegram":
                await self.telegram.start()
                self.active_interfaces.add("telegram")
            elif interface_name == "cli":
                self.cli.run()
                self.active_interfaces.add("cli")
            else:
                raise ValueError(f"Unknown interface: {interface_name}")
        except Exception as e:
            self.logger.error(f"Failed to start {interface_name}: {str(e)}")
            raise

    async def stop_all(self):
        """Gracefully shutdown all interfaces"""
        if "telegram" in self.active_interfaces:
            await self.telegram.stop()
        # Other interfaces can be added here
        self.active_interfaces.clear()

class WebInterface:
    """Unified web interface combining FastAPI and Flask"""
    def __init__(self, core):
        self.core = core
        self.app = FastAPI(title="SLICK AI Dashboard")
        self.flask_app = self._create_flask_app()
        
        # Setup routes and static files
        self._setup_routes()
        self._mount_assets()

    def _create_flask_app(self):
        """Create Flask app for legacy routes"""
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/legacy/chat', methods=['POST'])
        def legacy_chat():
            return {"status": "Use /api/chat instead"}
            
        return app

    def _setup_routes(self):
        """Configure all API routes"""
        router = APIRouter()
        
        @router.post("/api/chat")
        async def chat_handler(message: str):
            return await self.core.process(message)
            
        self.app.include_router(router)

    def _mount_assets(self):
        """Mount static files"""
        static_path = Path(__file__).parent.parent / "web_interface/static"
        self.app.mount("/static", StaticFiles(directory=static_path), name="static")

    def run(self):
        """Run both FastAPI and Flask servers"""
        import threading
        
        # Run Flask in background thread
        flask_thread = threading.Thread(
            target=self.flask_app.run,
            kwargs={"host": "0.0.0.0", "port": 5000},
            daemon=True
        )
        flask_thread.start()
        
        # Run FastAPI in main thread
        uvicorn.run(self.app, host="0.0.0.0", port=8000)

class TelegramInterface:
    """Enhanced Telegram bot interface"""
    def __init__(self, core):
        self.core = core
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.logger = logging.getLogger('TelegramBot')
        self.app = self._initialize_bot()

    def _initialize_bot(self):
        """Validate and create bot application"""
        if not self._is_valid_token(self.token):
            raise ValueError("Invalid Telegram token format")
            
        app = Application.builder().token(self.token).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", self._start_command))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))
        
        return app

    async def _start_command(self, update, context):
        await update.message.reply_text('🚀 SLICK AI is ready! How can I assist you?')

    async def _handle_message(self, update, context):
        try:
            response = await self.core.process(update.message.text)
            await update.message.reply_text(response)
        except Exception as e:
            self.logger.error(f"Message processing error: {str(e)}")
            await update.message.reply_text("⚠️ Error processing your request")

    async def start(self):
        """Start the bot"""
        self.logger.info("Starting Telegram bot...")
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()

    async def stop(self):
        """Stop the bot gracefully"""
        self.logger.info("Stopping Telegram bot...")
        if self.app.updater and self.app.updater.running:
            await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()

class VoiceInterface:
    """Voice recognition and synthesis"""
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.logger = logging.getLogger('VoiceInterface')

    def listen(self) -> Optional[str]:
        """Capture and transcribe voice input"""
        try:
            with self.microphone as source:
                self.logger.debug("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source)
                self.logger.debug("Listening...")
                audio = self.recognizer.listen(source, timeout=5)
                return self.recognizer.recognize_google(audio)
        except Exception as e:
            self.logger.error(f"Voice recognition error: {str(e)}")
            return None

    def speak(self, text: str):
        """Synthesize speech output"""
        # Implementation would use a TTS engine
        self.logger.info(f"Speaking: {text}")

class CLIInterface:
    """Command Line Interface"""
    def __init__(self, core):
        self.core = core
        self.logger = logging.getLogger('CLIInterface')

    def run(self):
        """Run the interactive CLI"""
        print("SLICK AI CLI - Type 'exit' to quit")
        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() == 'exit':
                    break
                    
                response = asyncio.run(self.core.process(user_input))
                print(f"Slick: {response}")
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.logger.error(f"CLI error: {str(e)}")
                print("Error processing input")

# ========================
# PROXY CONFIGURATION
# ========================

class ProxyConfig:
    """NGINX proxy configuration generator"""
    @staticmethod
    def generate_config():
        return """
        server {
            listen 80;
            server_name slick.yourdomain.com;
            
            location / {
                proxy_pass http://localhost:8080;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
            }
            
            location /api/ {
                proxy_pass http://localhost:8000;
                proxy_set_header X-Real-IP $remote_addr;
            }
            
            location /ws {
                proxy_pass http://localhost:8000;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
            }
        }
        """

# ========================
# MAIN APPLICATION
# ========================

if __name__ == "__main__":
    # Example usage
    from slick.core import SlickCore  # Your main AI core
    
    logging.basicConfig(level=logging.INFO)
    core = SlickCore()
    manager = InterfaceManager(core)
    
    try:
        # Start desired interfaces
        asyncio.run(manager.start_interface("web"))
        asyncio.run(manager.start_interface("telegram"))
    except KeyboardInterrupt:
        asyncio.run(manager.stop_all())