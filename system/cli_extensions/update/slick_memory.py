cat > slick/memory.py << 'EOF'
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
    
    Args:
        storage_path: Path to the memory storage file.
        
    Returns:
        Initialized memory bank.
    """
    global MEMORY_BANK
    
    try:
        if os.path.exists(storage_path):
            with open(storage_path, 'r') as f:
                MEMORY_BANK = json.load(f)
        else:
            # Create a new memory bank with default structure
            MEMORY_BANK = {
                "short_term": {},
                "long_term": {},
                "associative": {}
            }
            save_memory(storage_path)
            
    except Exception as e:
        print(f"Error initializing memory: {e}")
        # Fall back to empty memory structure
        MEMORY_BANK = {
            "short_term": {},
            "long_term": {},
            "associative": {}
        }
    
    return MEMORY_BANK

def save_memory(storage_path: str = "memory_data.json") -> bool:
    """
    Save the current memory state to disk.
    
    Args:
        storage_path: Path to save the memory data.
        
    Returns:
        True if save was successful, False otherwise.
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
    Apply a bias to the memory system (e.g., recency, frequency, importance).
    
    Args:
        bias_name: Name of the bias to apply.
        bias_value: Strength of the bias.
    """
    # This would be implemented based on your specific memory biasing needs
    # For now, we'll just store it in the memory bank
    if "biases" not in MEMORY_BANK:
        MEMORY_BANK["biases"] = {}
    MEMORY_BANK["biases"][bias_name] = bias_value

def retrieve_memory(key: str, memory_type: str = "long_term") -> Any:
    """
    Retrieve a memory by key.
    
    Args:
        key: Key to look up in memory.
        memory_type: Which memory bank to access ('short_term', 'long_term', 'associative').
        
    Returns:
        The stored value or None if not found.
    """
    return MEMORY_BANK.get(memory_type, {}).get(key)

def store_memory(key: str, value: Any, memory_type: str = "long_term") -> None:
    """
    Store a memory.
    
    Args:
        key: Key to store the memory under.
        value: Value to store.
        memory_type: Which memory bank to use ('short_term', 'long_term', 'associative').
    """
    if memory_type not in MEMORY_BANK:
        MEMORY_BANK[memory_type] = {}
    MEMORY_BANK[memory_type][key] = value

# Initialize memory when module is imported
initialize_memory()
EOF