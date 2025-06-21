# logic/commands/command_utils.py
from pathlib import Path
from typing import Union

def validate_path(path: Union[str, Path]) -> Path:
    """Validate and normalize a path"""
    path = Path(path).resolve()
    if not path.exists():
        raise ValueError(f"Path does not exist: {path}")
    return path

def confirm_action(prompt: str) -> bool:
    """Get user confirmation"""
    response = input(f"{prompt} [y/N]: ").strip().lower()
    return response == 'y'