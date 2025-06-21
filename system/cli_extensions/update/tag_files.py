import os
import re
from pathlib import Path

TAG_RULES = {
    # Regex patterns with corresponding tags
    r"(orchestrator|slick_core)\.py": "🟢 USE",
    r"(adapter|integration)\.py": "🟢 USE",
    r"_v\d+\.py|/archive/": "🔵 SAVE",
    r"(training|knowledge)\.py": "🟠 MERGE",
    r"(deprecated|legacy|old_)": "🔴 DELETE",
    r"(__pycache__|\.log|\.tmp)": "⚫ IGNORE"
}

def tag_file(filepath: Path):
    content = filepath.read_text()
    for pattern, tag in TAG_RULES.items():
        if re.search(pattern, str(filepath)):
            if "# STATUS:" not in content:
                new_content = f"# STATUS: {tag} - {tag.split(' ')[1]} file\n{content}"
                filepath.write_text(new_content)
                print(f"Tagged {filepath}: {tag}")
            return

for root, _, files in os.walk("."):
    for f in files:
        if f.endswith(".py"):  # Add other extensions as needed
            tag_file(Path(root) / f)