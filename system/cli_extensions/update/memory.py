"""
slick/memory.py - Memory management module for Slick AI system
"""

from typing import Dict, Any
import json
import os

# Memory bank structure
MEMORY_BANK: Dict[str, Any] = {
    "short_term": {},
    "long_term": {},
    "associative": {}
}

def initialize_memory(storage_path: str = "memory_data.json") -> Dict[str, Any]:
    """
    Initialize the memory system by loading from disk or creating a new memory bank.
    """
    global MEMORY_BANK
    
    try:
        if os.path.exists(storage_path):
            with open(storage_path, 'r') as f:
                MEMORY_BANK = json.load(f)
        else:
            MEMORY_BANK = {
                "short_term": {},
                "long_term": {},
                "associative": {}
            }
            save_memory(storage_path)
    except Exception as e:
        print(f"Error initializing memory: {e}")
        MEMORY_BANK = {
            "short_term": {},
            "long_term": {},
            "associative": {}
        }
    
    return MEMORY_BANK

def save_memory(storage_path: str = "memory_data.json") -> bool:
    """
    Save the current memory state to disk.
    """
    try:
        with open(storage_path, 'w') as f:
            json.dump(MEMORY_BANK, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving memory: {e}")
        return False

def apply_memory_bias(bias_name: str, bias_value: float) -> None:
    """
    Apply a bias to the memory system.
    """
    if "biases" not in MEMORY_BANK:
        MEMORY_BANK["biases"] = {}
    MEMORY_BANK["biases"][bias_name] = bias_value

# Initialize memory when module is imported
initialize_memory()
