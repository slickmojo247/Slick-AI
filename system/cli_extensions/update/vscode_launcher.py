# dev_env/vscode_launcher.py
import subprocess
from pathlib import Path

class VSCodeDevUI:
    def __init__(self, core):
        self.project_root = Path(__file__).parent.parent
        
    def launch(self):
        subprocess.run([
            "code", str(self.project_root),
            "--extension-dir", str(self.project_root/"dev_env/vscode_extensions")
        ])