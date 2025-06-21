from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter()

# Load proxy config from adjacent JSON file
proxy_config = json.loads(
    (Path(__file__).parent / "Proxy_Server.json").read_text()
)

@router.get("/proxy")
async def get_proxy_settings():
    return proxy_config

@router.post("/proxy/update")
async def update_proxy(config: dict):
    # Add your proxy update logic here
    return {"status": "success"}