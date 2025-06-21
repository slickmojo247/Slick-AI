import pickle
import zlib
from pathlib import Path

class MemoryResetManager:
    def __init__(self, memory_bank):
        self.memory = memory_bank
        self.save_dir = Path("memory_saves")
        
    def prepare_reset(self, reset_type):
        save_path = self.save_dir / f"reset_{reset_type}.pkl"
        with open(save_path, 'wb') as f:
            data = zlib.compress(pickle.dumps(self.memory.long_term))
            f.write(data)
        
        if reset_type == "hard":
            self.memory.long_term = {}
        return str(save_path)