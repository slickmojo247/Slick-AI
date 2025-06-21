# slick/memory/progress_manager.py
import json
import pickle
import zlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import hashlib
from concurrent.futures import ThreadPoolExecutor

class MemoryProgressManager:
    """Enhanced memory progress saver with compression and versioning"""
    
    def __init__(self, save_dir: str = "memory_saves"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.current_save_version = "1.2"
        self.executor = ThreadPoolExecutor(max_workers=2)
        
    def save_memory_state(self, 
                        memory_bank: Dict[str, Any], 
                        immediate: bool = False) -> str:
        """
        Save memory state with progress tracking
        Args:
            memory_bank: The memory dictionary to save
            immediate: If True, saves synchronously
        Returns:
            Path to the save file
        """
        save_data = {
            'version': self.current_save_version,
            'timestamp': datetime.now().isoformat(),
            'memory': memory_bank,
            'checksum': self._calculate_memory_checksum(memory_bank)
        }
        
        save_path = self._generate_save_path()
        
        if immediate:
            return self._save_to_disk(save_path, save_data)
        else:
            self.executor.submit(self._save_to_disk, save_path, save_data)
            return str(save_path)
    
    def load_memory_state(self, 
                         save_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load memory state from save file
        Args:
            save_path: Optional specific path to load from
        Returns:
            The loaded memory bank
        """
        if save_path is None:
            save_path = self._find_latest_save()
            
        if not Path(save_path).exists():
            raise FileNotFoundError(f"No save file found at {save_path}")
            
        with open(save_path, 'rb') as f:
            compressed = f.read()
            try:
                save_data = pickle.loads(zlib.decompress(compressed))
            except Exception as e:
                raise ValueError(f"Failed to load save file: {str(e)}")
                
        # Verify checksum
        current_checksum = self._calculate_memory_checksum(save_data['memory'])
        if current_checksum != save_data['checksum']:
            raise ValueError("Memory checksum verification failed - data may be corrupted")
            
        return save_data['memory']
    
    def _save_to_disk(self, save_path: Path, save_data: Dict) -> str:
        """Internal method to handle actual file saving"""
        try:
            compressed = zlib.compress(pickle.dumps(save_data))
            temp_path = save_path.with_suffix('.tmp')
            
            with open(temp_path, 'wb') as f:
                f.write(compressed)
            
            # Atomic write operation
            temp_path.replace(save_path)
            return str(save_path)
        except Exception as e:
            print(f"Error saving memory: {str(e)}")
            raise
    
    def _generate_save_path(self) -> Path:
        """Generate timestamped save path"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.save_dir / f"memory_save_{timestamp}.msav"
    
    def _find_latest_save(self) -> str:
        """Find most recent save file"""
        saves = list(self.save_dir.glob("memory_save_*.msav"))
        if not saves:
            raise FileNotFoundError("No save files found")
        return str(max(saves, key=lambda f: f.stat().st_mtime))
    
    def _calculate_memory_checksum(self, memory_bank: Dict) -> str:
        """Calculate SHA256 checksum of memory contents"""
        sha256 = hashlib.sha256()
        # Convert memory to bytes in consistent order
        memory_bytes = json.dumps(memory_bank, sort_keys=True).encode('utf-8')
        sha256.update(memory_bytes)
        return sha256.hexdigest()
    
    def get_save_versions(self) -> Dict[str, Dict]:
        """Get metadata for all available saves"""
        saves = {}
        for save_file in self.save_dir.glob("memory_save_*.msav"):
            with open(save_file, 'rb') as f:
                try:
                    metadata = pickle.loads(zlib.decompress(f.read()))
                    saves[str(save_file)] = {
                        'version': metadata.get('version'),
                        'timestamp': metadata.get('timestamp'),
                        'size': save_file.stat().st_size
                    }
                except:
                    continue
        return saves
    
    def cleanup_old_saves(self, max_saves: int = 10) -> None:
        """Keep only the most recent saves"""
        saves = sorted(self.save_dir.glob("memory_save_*.msav"), 
                      key=lambda f: f.stat().st_mtime, 
                      reverse=True)
        for old_save in saves[max_saves:]:
            old_save.unlink()

# Integration with existing memory system
def save_memory_progress(memory_bank: Dict[str, Any], 
                        immediate: bool = False) -> str:
    """
    Public interface for saving memory progress
    Args:
        memory_bank: The memory dictionary from slick.memory
        immediate: If True, blocks until save completes
    Returns:
        Path to the save file
    """
    manager = MemoryProgressManager()
    return manager.save_memory_state(memory_bank, immediate)

def load_memory_progress(save_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Public interface for loading memory progress
    Args:
        save_path: Optional specific save file to load
    Returns:
        The loaded memory bank
    """
    manager = MemoryProgressManager()
    return manager.load_memory_state(save_path)