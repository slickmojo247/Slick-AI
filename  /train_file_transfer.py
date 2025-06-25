import os
import shutil
from pathlib import Path

class FileTransferTrainer:
    def __init__(self):
        self.source = Path.home() / "Slick_AI"
        self.target = Path.home() / "Slick_Mojo"
        self.rules = {
            "exclude": [".git", "env.json", "session_logs"],
            "overwrite": False
        }
    
    def train_transfer(self, file_patterns):
        """Train Slick to recognize file types and their destinations"""
        for pattern in file_patterns:
            for file in self.source.rglob(pattern):
                rel_path = file.relative_to(self.source)
                target_path = self.target / rel_path
                
                # Apply training rules
                if any(excl in str(rel_path) for excl in self.rules["exclude"]):
                    print(f"⏩ Skipping excluded: {rel_path}")
                    continue
                    
                if target_path.exists() and not self.rules["overwrite"]:
                    print(f"⚠️ Exists (not overwriting): {rel_path}")
                    continue
                
                # Demonstrate the copy operation
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, target_path)
                print(f"✅ Copied: {rel_path}")

# Training session
if __name__ == "__main__":
    trainer = FileTransferTrainer()
    print("=== Training File Transfer ===")
    
    # Train with specific file patterns (expand as needed)
    trainer.train_transfer([
        "*.py",          # All Python files
        "config/*.json", # Config files (but not env.json)
        "core/*.md"      # Documentation
    ])