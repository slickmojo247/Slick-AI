"""
SLICK AI - Unified Control System
Combines:
- AI integration (OpenAI/DeepSeek)
- Command management
- Configuration system
- Web interface (FastAPI/Flask)
"""

import os
import re
import json
import csv
import logging
import sqlite3
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Literal
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, WebSocket, HTTPException
from flask import Flask, jsonify
import httpx
import uvicorn

# ========================
# CORE CONFIGURATION
# ========================

class Config:
    """Unified configuration system"""
    def __init__(self):
        load_dotenv()
        self.settings = {
            'OPENAI_API_KEY': os.getenv("OPENAI_API_KEY"),
            'DEEPSEEK_API_KEY': os.getenv("DEEPSEEK_API_KEY"),
            'TELEGRAM_TOKEN': os.getenv("TELEGRAM_BOT_TOKEN"),
            'FLASK_HOST': os.getenv("FLASK_RUN_HOST", "0.0.0.0"),
            'FLASK_PORT': int(os.getenv("FLASK_RUN_PORT", 5000)),
            'DEBUG': os.getenv("SLICK_DEBUG", "True") == "True"
        }
        
    def verify(self):
        """Verify all required configurations are present"""
        required = ['OPENAI_API_KEY', 'DEEPSEEK_API_KEY']
        return all(self.settings[key] for key in required)

# ========================
# AI INTEGRATION
# ========================

class AIIntegration:
    """Unified AI service manager"""
    def __init__(self, config):
        self.config = config
        self.knowledge_base = self._load_knowledge_base()
        self.sessions = {}  # {session_id: [messages]}
        
    def _load_knowledge_base(self):
        try:
            with open('knowledge_base.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"slick_ai": {}, "chatgpt": {}, "deepseek": {}}
            
    def _save_knowledge_base(self):
        with open('knowledge_base.json', 'w') as f:
            json.dump(self.knowledge_base, f, indent=2)
            
    async def query_openai(self, prompt, context=None, model="gpt-4"):
        if not self.config.settings['OPENAI_API_KEY']:
            raise ValueError("OpenAI API key not configured")
            
        headers = {
            "Authorization": f"Bearer {self.config.settings['OPENAI_API_KEY']}",
            "Content-Type": "application/json"
        }
        
        messages = [{"role": "user", "content": prompt}]
        if context:
            messages.insert(0, {"role": "system", "content": context})
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": 500,
                    "temperature": 0.7
                }
            )
            return response.json()["choices"][0]["message"]["content"]
            
    async def query_deepseek(self, prompt, context=None, model="deepseek-coder"):
        if not self.config.settings['DEEPSEEK_API_KEY']:
            raise ValueError("DeepSeek API key not configured")
            
        headers = {
            "Authorization": f"Bearer {self.config.settings['DEEPSEEK_API_KEY']}",
            "Content-Type": "application/json"
        }
        
        full_prompt = "You are a Slick AI assistant.\n\n"
        if context:
            full_prompt += f"Context: {context}\n\n"
        full_prompt += f"Question: {prompt}"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": full_prompt}],
                    "max_tokens": 500,
                    "temperature": 0.7
                }
            )
            return response.json()["choices"][0]["message"]["content"]
            
    async def query(self, prompt, model="hybrid", session_id=None):
        """Unified query interface"""
        session = self.sessions.setdefault(session_id, [])
        session.append({"role": "user", "content": prompt})
        
        # Get relevant context from knowledge base
        context = "\n".join(
            f"{k}: {v}" for source in self.knowledge_base.values()
            for k, v in source.items() if k.lower() in prompt.lower()
        )
        
        # Route query based on model selection
        if model == "hybrid":
            model = "deepseek-coder" if ("code" in prompt or "debug" in prompt) else "gpt-4"
            
        if "deepseek" in model:
            result = await self.query_deepseek(prompt, context, model)
        else:
            result = await self.query_openai(prompt, context, model)
            
        # Store result in knowledge base
        self.knowledge_base[model][prompt] = result
        self._save_knowledge_base()
        
        # Add to session history
        session.append({"role": "assistant", "content": result})
        return result

# ========================
# COMMAND SYSTEM
# ========================

class CommandManager:
    """Unified command registry and management"""
    def __init__(self):
        self.commands = {
            "CURE": {
                "description": "Restore player health to maximum",
                "status": False,
                "dependencies": ["requests", "boto3"],
                "color": "#FF6B6B",
                "icon": "fa-heartbeat"
            },
            "LOOK": {
                "description": "Enable cosmic vision",
                "status": False,
                "dependencies": ["requests", "pusher"],
                "color": "#4ECDC4",
                "icon": "fa-eye"
            }
        }
        
    def get_command(self, name):
        return self.commands.get(name)
        
    def get_all_commands(self):
        return self.commands
        
    def toggle_command(self, name):
        if name not in self.commands:
            raise ValueError(f"Command '{name}' not found")
        self.commands[name]["status"] = not self.commands[name]["status"]
        return self.commands[name]["status"]
        
    def add_command(self, name, description, dependencies=None):
        if name in self.commands:
            raise ValueError(f"Command '{name}' already exists")
        self.commands[name] = {
            "description": description,
            "status": False,
            "dependencies": dependencies or [],
            "color": "#FFFFFF",
            "icon": "fa-cog"
        }
        
    def remove_command(self, name):
        if name not in self.commands:
            raise ValueError(f"Command '{name}' not found")
        del self.commands[name]

# ========================
# WEB INTERFACE
# ========================

class WebService:
    """Unified web interface (FastAPI + Flask)"""
    def __init__(self, config, ai, command_manager):
        self.config = config
        self.ai = ai
        self.command_manager = command_manager
        
        # Initialize FastAPI
        self.fastapi_app = FastAPI()
        self.api_router = APIRouter()
        self._setup_fastapi_routes()
        
        # Initialize Flask
        self.flask_app = Flask(__name__)
        self._setup_flask_routes()
        
    def _setup_fastapi_routes(self):
        @self.api_router.post("/ai/query")
        async def ai_query(prompt: str, model: str = "hybrid"):
            try:
                result = await self.ai.query(prompt, model)
                return {"response": result}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
                
        @self.api_router.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            while True:
                data = await websocket.receive_json()
                response = await self.ai.query(data['message'])
                await websocket.send_json({"response": response})
                
        self.fastapi_app.include_router(self.api_router)
        
    def _setup_flask_routes(self):
        @self.flask_app.route('/')
        def home():
            return 'SLICK AI Control Center'
            
        @self.flask_app.route('/commands')
        def list_commands():
            return jsonify(self.command_manager.get_all_commands())
            
        @self.flask_app.route('/commands/<name>/toggle', methods=['POST'])
        def toggle_command(name):
            try:
                new_status = self.command_manager.toggle_command(name)
                return jsonify({
                    "status": "success",
                    "command": name,
                    "enabled": new_status
                })
            except ValueError as e:
                return jsonify({"status": "error", "message": str(e)}), 404
                
    def run(self):
        """Run both servers"""
        # Run FastAPI in a separate thread
        import threading
        fastapi_thread = threading.Thread(
            target=uvicorn.run,
            args=(self.fastapi_app,),
            kwargs={"host": "0.0.0.0", "port": 8000},
            daemon=True
        )
        fastapi_thread.start()
        
        # Run Flask in main thread
        self.flask_app.run(
            host=self.config.settings['FLASK_HOST'],
            port=self.config.settings['FLASK_PORT'],
            debug=self.config.settings['DEBUG']
        )

# ========================
# MAIN APPLICATION
# ========================

def main():
    # Initialize configuration
    config = Config()
    if not config.verify():
        print("⚠️ Missing required configuration. Please check your environment variables.")
        return
        
    # Initialize components
    ai = AIIntegration(config)
    command_manager = CommandManager()
    
    # Create and run web service
    web_service = WebService(config, ai, command_manager)
    web_service.run()

if __name__ == "__main__":
    main()