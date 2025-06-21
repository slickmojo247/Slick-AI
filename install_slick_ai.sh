#!/bin/bash

# Slick AI System Installation Script
# Run this from your new project directory

echo "🚀 Starting Slick AI System Installation..."

# 1. Create directory structure
echo "📂 Creating directory structure..."
mkdir -p \
  ai_core \
  app \
  backend \
  cli \
  cognitive \
  config \
  core \
  data \
  deployment \
  docs \
  engine \
  interfaces/{web,voice,vscode} \
  knowledge \
  memory \
  modules \
  scripts \
  slick \
  system \
  tests \
  utils

# 2. Check for and install Python dependencies
echo "🐍 Checking Python dependencies..."
REQUIREMENTS="requirements.txt"
if [ ! -f "$REQUIREMENTS" ]; then
  echo "📝 Creating default requirements.txt..."
  cat > "$REQUIREMENTS" <<EOL
fastapi==0.95.2
uvicorn==0.22.0
openai==0.28.1
python-telegram-bot==20.3
flask==2.3.2
numpy==1.24.3
pandas==2.0.2
python-dotenv==1.0.0
watchdog==3.0.0
click==8.1.3
pytest==7.4.0
websockets==11.0.3
networkx==3.1
scikit-learn==1.3.0
EOL
fi

echo "🔧 Installing Python packages..."
pip install -r "$REQUIREMENTS"

# 3. Install system dependencies
echo "🛠️ Checking for system dependencies..."
declare -A DEPS=(
  ["rsync"]="rsync"
  ["git"]="git"
  ["ffmpeg"]="ffmpeg"  # For voice processing
)

for dep in "${!DEPS[@]}"; do
  if ! command -v "$dep" &> /dev/null; then
    echo "⚠️ $dep not found. Installing..."
    sudo apt-get install -y "${DEPS[$dep]}"
  fi
done

# 4. Set up core configuration files
echo "⚙️ Setting up configuration files..."

# .env file
if [ ! -f ".env" ]; then
  echo "🔐 Creating .env file..."
  cat > .env <<EOL
# Slick AI Configuration
SLICK_ENV=development
OPENAI_API_KEY=your_openai_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here
TELEGRAM_BOT_TOKEN=your_bot_token_here
MEMORY_DECAY_RATE=0.15
DEFAULT_PERSONALITY=balanced
EOL
  echo "ℹ️ Please edit the .env file with your actual API keys"
fi

# config/blend_settings.ini
if [ ! -f "config/blend_settings.ini" ]; then
  echo "🎛️ Creating blend settings config..."
  mkdir -p config
  cat > config/blend_settings.ini <<EOL
[blending]
mode = balanced
weight_openai = 0.7
weight_deepseek = 0.3
fallback_source = deepseek
creativity = 0.8
precision = 0.9
strictness = 0.7

[personality]
default_mode = balanced
available_modes = balanced,technical,creative,homer
EOL
fi

# 5. Set up core Python files
echo "💻 Setting up core Python files..."

# main.py
if [ ! -f "main.py" ]; then
  echo "📄 Creating main.py entry point..."
  cat > main.py <<EOL
#!/usr/bin/env python3
"""
Slick AI System Main Entry Point
"""

from ai_core.AIOrchestrator import AIOrchestrator
from memory.MemoryBank import MemoryBank
import logging

def initialize_system():
    """Initialize the Slick AI system components"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("🚀 Initializing Slick AI System...")
        
        # Initialize memory system
        memory = MemoryBank()
        
        # Initialize AI orchestrator
        orchestrator = AIOrchestrator(memory)
        
        logger.info("✅ System initialized successfully")
        return orchestrator
    
    except Exception as e:
        logger.error(f"❌ Failed to initialize system: {e}")
        raise

if __name__ == "__main__":
    system = initialize_system()
    # Add your main loop here
EOL
chmod +x main.py
fi

# 6. Install optional components
echo "🔍 Checking for optional components..."

# Voice interface setup
if [ ! -d "interfaces/voice" ]; then
  echo "🎤 Setting up voice interface..."
  mkdir -p interfaces/voice
  # Add basic voice interface files
  cat > interfaces/voice/voice_server.py <<EOL
# Voice interface implementation
import sounddevice as sd
import numpy as np

class VoiceInterface:
    def __init__(self):
        self.sample_rate = 16000
        self.channels = 1
        
    def start_listening(self, callback):
        """Start listening for voice input"""
        def audio_callback(indata, frames, time, status):
            if status:
                print(status)
            callback(indata.copy())
        
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=audio_callback
        ):
            print("🎤 Voice interface ready...")
            while True:
                pass
EOL
fi

# 7. Finalize installation
echo "✨ Finalizing installation..."

# Create default memory directory
mkdir -p data/memory

# Set up basic test
if [ ! -f "tests/test_basic.py" ]; then
  echo "🧪 Creating basic test..."
  mkdir -p tests
  cat > tests/test_basic.py <<EOL
import unittest
from ..core import SystemInitializer

class TestBasicSetup(unittest.TestCase):
    def test_system_init(self):
        """Test that the system can initialize"""
        system = SystemInitializer()
        self.assertTrue(system.is_initialized())

if __name__ == '__main__':
    unittest.main()
EOL
fi

echo "🎉 Installation complete!"
echo "➡️ Next steps:"
echo "1. Edit .env with your API keys"
echo "2. Run 'python main.py' to start the system"
echo "3. Run 'pytest' to verify the installation"