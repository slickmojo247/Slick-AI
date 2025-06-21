# Merges: app.py, main.py, ai.py, security.py
from fastapi import FastAPI, Security
from security import APIKeyHeader

app = FastAPI()
auth = APIKeyHeader(name="X-API-KEY")

@app.post("/ai/route")
async def route_request(prompt: str, provider: str = "auto"):
    """Routes to OpenAI (general) or Deepseek (code)"""
    provider = "deepseek" if any(kw in prompt.lower() for kw in ["code", "debug"]) else "openai"
    return await globals()[f"{provider}_handler"](prompt)

@app.get("/system/status")
def status():
    return {
        "services": ["ai", "telegram", "vscode"],
        "memory": f"{psutil.virtual_memory().percent}% used"
    }