# assessment_script.py
import os
from pathlib import Path

def analyze_new_folders(base_dir="slick_ai_system"):
    new_folders = []
    existing = ["core", "interface", "knowledge", "memory"] # Your current folders
    
    for item in os.listdir(base_dir):
        if os.path.isdir(item) and item not in existing:
            new_folders.append(item)
    
    print("New folders detected:")
    for folder in new_folders:
        size = sum(f.stat().st_size for f in Path(folder).rglob('*') if f.is_file())
        print(f"📁 {folder} ({size/1024:.1f} KB)")
    
    return new_folders