import json
import zlib
import pickle
from pathlib import Path
from datetime import datetime
from cryptography.fernet import Fernet

class MemoryPersistence:
    def __init__(self, encryption_key=None):
        self.save_dir = Path("memory_states")
        self.save_dir.mkdir(exist_ok=True)
        self.cipher = Fernet(encryption_key) if encryption_key else None
        
    def save_state(self, memory_data, reset_type="soft"):
        """Save memory state with reset type metadata"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = self.save_dir / f"reset_{reset_type}_{timestamp}.mem"
        
        state = {
            "metadata": {
                "reset_type": reset_type,
                "timestamp": datetime.now().isoformat(),
                "memory_size": len(memory_data)
            },
            "data": memory_data
        }
        
        # Serialize and compress
        serialized = pickle.dumps(state)
        compressed = zlib.compress(serialized)
        
        # Encrypt if key provided
        if self.cipher:
            compressed = self.cipher.encrypt(compressed)
        
        with open(save_path, "wb") as f:
            f.write(compressed)
            
        return save_path

    def load_state(self, save_path, reset_type="soft"):
        """Load specific memory state"""
        with open(save_path, "rb") as f:
            compressed = f.read()
        
        if self.cipher:
            compressed = self.cipher.decrypt(compressed)
        
        serialized = zlib.decompress(compressed)
        return pickle.loads(serialized)

    def get_available_resets(self):
        """List all saved reset points"""
        return sorted(self.save_dir.glob("reset_*.mem"), 
                      key=lambda x: x.stat().st_mtime, 
                      reverse=True)

class MemoryResetManager:
    def __init__(self, memory_bank):
        self.memory = memory_bank
        self.persistence = MemoryPersistence()
        
    def prepare_reset(self, reset_type="soft"):
        # Create pre-reset snapshot
        save_path = self.persistence.save_state(
            self.memory.long_term,
            reset_type
        )
        
        # Clear memory based on reset type
        if reset_type == "hard":
            self.memory.long_term = {}
            self.memory.code_snippets = {'python': {}, 'json': {}, 'js': {}, 'html': {}}
        else:  # soft reset
            self.memory.apply_decay(aggressive=True)
            
        return save_path

    def restore_state(self, save_path):
        """Restore memory from specific save"""
        state = self.persistence.load_state(save_path)
        self.memory.long_term = state["data"]
        return state["metadata"]