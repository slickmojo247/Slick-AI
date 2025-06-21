#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime

def sync_project():
    print("Starting system sync...")
    
    # 1. Git operations
    print("\nSyncing git repository...")
    subprocess.run(['git', 'pull'])
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', f"Auto-sync {datetime.now().isoformat()}"])
    subprocess.run(['git', 'push'])
    
    # 2. Reorganize components
    print("\nReorganizing components...")
    # Move streamline_ai.py
    if os.path.exists('streamline_ai.py'):
        os.rename('streamline_ai.py', 'core/ai_models/streamline_ai.py')
    
    # Move AI_MEMORY.PY
    game_mem_path = 'slick/SLICK_AI/game_ai/AI_MEMORY.PY'
    if os.path.exists(game_mem_path):
        os.rename(game_mem_path, 'app/memory/game_memory.py')
    
    # 3. Restructure mic_input
    if os.path.exists('mic_input'):
        os.makedirs('app/input', exist_ok=True)
        for item in os.listdir('mic_input'):
            os.rename(f'mic_input/{item}', f'app/input/{item}')
        os.rmdir('mic_input')
    
    # 4. Update requirements
    print("\nUpdating dependencies...")
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
    subprocess.run(['pip', 'install', '-r', 'backend/requirements.txt'])
    
    print("\nSync completed successfully!")

if __name__ == '__main__':
    sync_project()