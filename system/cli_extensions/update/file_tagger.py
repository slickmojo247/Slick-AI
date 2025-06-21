# app/core/file_tagger.py
import re
from pathlib import Path
from typing import Dict, List
import json

COLOR_SCHEME = {
    "USE": "#4CAF50",  # Green
    "SAVE": "#2196F3",  # Blue
    "MERGE": "#FF9800", # Orange
    "DELETE": "#F44336",# Red
    "IGNORE": "#9E9E9E" # Gray
}

class FileTagger:
    def __init__(self, project_root: str):
        self.root = Path(project_root)
        self.tag_rules = self._load_rules()
        
    def _load_rules(self) -> Dict[str, str]:
        """Load tagging rules from config"""
        rules_path = self.root / ".vscode" / "tag_rules.json"
        if rules_path.exists():
            with open(rules_path) as f:
                return json.load(f)
        return {
            "**/core/**/*.py": "USE",
            "**/adapters/**/*.py": "USE",
            "**/_v*.py": "SAVE",
            "**/deprecated/**": "DELETE",
            "**/__pycache__/**": "IGNORE"
        }

    def tag_file(self, file_path: Path) -> str:
        """Determine tag for a file"""
        rel_path = str(file_path.relative_to(self.root))
        
        for pattern, tag in self.tag_rules.items():
            if re.fullmatch(pattern.replace("**", ".*"), rel_path):
                return tag
        return "USE"  # Default

    def write_tag(self, file_path: Path, tag: str):
        """Write tag to file header"""
        content = file_path.read_text()
        
        # Remove existing tag if present
        content = re.sub(r"^# STATUS: .*\n", "", content, flags=re.MULTILINE)
        
        # Insert new tag after shebang/docstring
        lines = content.splitlines(keepends=True)
        insert_at = 0
        if lines and lines[0].startswith("#!"):  # Preserve shebang
            insert_at = 1
        
        lines.insert(insert_at, f"# STATUS: {tag} - {file_path.name}\n")
        file_path.write_text("".join(lines))

    def tag_project(self):
        """Tag all project files"""
        for py_file in self.root.rglob("*.py"):
            if py_file.is_file():
                tag = self.tag_file(py_file)
                self.write_tag(py_file, tag)
                print(f"Tagged {py_file.relative_to(self.root)} as {tag}")
