# test_websocket.py
import websockets
import asyncio
import json

async def test_ws():
    async with websockets.connect("ws://localhost:8000/ws/ai") as ws:
        await ws.send(json.dumps({
            "message": "Tell me a joke about AI",
            "mode": "homer"
        }))
        response = await ws.recv()
        print("Response:", json.loads(response))

asyncio.get_event_loop().run_until_complete(test_ws())