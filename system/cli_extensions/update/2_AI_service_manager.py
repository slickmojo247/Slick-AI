# Merges: openai.py, deepseek.py, deepseek_chat_manager.py
import openai, httpx

class AIManager:
    def __init__(self):
        self.sessions = {}  # {session_id: [messages]}
    
    async def chat(self, prompt, session_id=None, provider="openai"):
        session = self.sessions.setdefault(session_id, [])
        session.append({"role": "user", "content": prompt})
        
        if provider == "openai":
            resp = await openai.ChatCompletion.acreate(
                model="gpt-4", messages=session)
        else:  # Deepseek
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    json={"messages": session},
                    headers={"Authorization": f"Bearer {DEEPSEEK_KEY}"}
                )
        
        session.append(resp.choices[0].message)
        return resp.choices[0].message.content