# core/routing.py
from fastapi import APIRouter, WebSocket
from slick.core.controller import SlickController
from slick.utils.file_manager import FileManager

router = APIRouter()
controller = SlickController()
files = FileManager()

@router.post("/query")
async def process_query(prompt: str):
    return await controller.handle_request(prompt)

@router.websocket("/ws")
async def websocket_handler(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_json()
        response = await controller.handle_request(data['message'])
        await ws.send_json({'response': response})

@router.get("/files")
async def list_files(path: str = None):
    return files.get_tree(path)