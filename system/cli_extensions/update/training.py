from openai import OpenAI
from deepseek_api import DeepSeek

class AITrainer:
    def __init__(self):
        self.openai = OpenAI(api_key=os.getenv('OPENAI_KEY'))
        self.deepseek = DeepSeek(api_key=os.getenv('DEEPSEEK_KEY'))
        
    async def train_on_conversation(self, messages):
        # Process through both AI systems
        openai_res = self.openai.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        
        deepseek_res = self.deepseek.analyze(
            text=messages[-1]['content'],
            task="comprehension"
        )
        
        # Your custom training logic here
        return self._process_responses(openai_res, deepseek_res)