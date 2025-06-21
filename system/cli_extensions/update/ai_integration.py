# backend/ai_integration.py

import os
import json
import requests

try:
    import openai
except ImportError:
    openai = None

class AIIntegration:
    def __init__(self):
        # Load API keys from environment
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        self.deepseek_base_url = "https://api.deepseek.com/v1"

        # Optional: Warn if keys are missing
        if not self.openai_api_key:
            print("⚠️ OPENAI_API_KEY is missing.")
        if not self.deepseek_api_key:
            print("⚠️ DEEPSEEK_API_KEY is missing.")

        # Init knowledge base
        self.knowledge_base = {}
        self.load_knowledge_base()

    def load_knowledge_base(self):
        try:
            with open('knowledge_base.json', 'r') as f:
                self.knowledge_base = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.knowledge_base = {"slick_ai": {}, "chatgpt": {}, "deepseek": {}}

    def save_knowledge_base(self):
        with open('knowledge_base.json', 'w') as f:
            json.dump(self.knowledge_base, f, indent=2)

    def query_chatgpt(self, prompt, context=None, model="gpt-4"):
        if not self.openai_api_key or not openai:
            return "OpenAI API not available."

        openai.api_key = self.openai_api_key

        messages = [
            {"role": "system", "content": "You are a Slick AI assistant specialized in game development."},
            {"role": "user", "content": context or ""},
            {"role": "user", "content": prompt}
        ]

        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"ChatGPT error: {str(e)}"

    def query_deepseek(self, prompt, context=None, model="deepseek-coder"):
        if not self.deepseek_api_key:
            return "DeepSeek API key not available."

        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }

        full_prompt = "You are a Slick AI assistant specialized in game tools.\n\n"
        if context:
            full_prompt += f"Context: {context}\n\n"
        full_prompt += f"Question: {prompt}"

        data = {
            "model": model,
            "messages": [{"role": "user", "content": full_prompt}],
            "max_tokens": 500,
            "temperature": 0.7
        }

        try:
            response = requests.post(
                f"{self.deepseek_base_url}/chat/completions",
                headers=headers,
                json=data
            )
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"DeepSeek error: {str(e)}"

    def add_to_knowledge_base(self, source, key, value):
        if source not in self.knowledge_base:
            self.knowledge_base[source] = {}
        self.knowledge_base[source][key] = value
        self.save_knowledge_base()

    def search_knowledge_base(self, query):
        results = []
        for source, data in self.knowledge_base.items():
            for key, val in data.items():
                if query.lower() in key.lower() or query.lower() in val.lower():
                    results.append({"source": source, "key": key, "value": val})
        return results

    def ai_assistant_query(self, query, model="hybrid"):
        context = "\n".join([f"{res['source']}: {res['value']}" for res in self.search_knowledge_base(query)])

        if model == "chatgpt":
            return self.query_chatgpt(query, context)
        elif model == "deepseek":
            return self.query_deepseek(query, context)
        else:
            gpt_response = self.query_chatgpt(query, context)
            if "code" in query or "debug" in query:
                ds_response = self.query_deepseek(query, context)
                combined = f"ChatGPT:\n{gpt_response}\n\nDeepSeek:\n{ds_response}"
                self.add_to_knowledge_base("hybrid", query, combined)
                return combined
            self.add_to_knowledge_base("chatgpt", query, gpt_response)
            return gpt_response
