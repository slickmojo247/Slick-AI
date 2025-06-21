from flask import Flask
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Debug: Print loaded keys to confirm they're being read
print("✅ OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
print("✅ DEEPSEEK_API_KEY:", os.getenv("DEEPSEEK_API_KEY"))

# AI Integration (optional)
try:
    from ai_integration import AIIntegration
    ai = AIIntegration()
except Exception as e:
    print(f"AI Integration Error: {e}")
    ai = None

# Flask App
app = Flask(__name__)

@app.route('/')
def home():
    return 'SLICK_AI backend is running.'

if __name__ == '__main__':
    app.run(debug=True)
