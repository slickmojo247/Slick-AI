# Maintenance Scheduler
import time
import threading
from slick.memory.memory_core import MemoryBank

class MaintenanceScheduler:
    def __init__(self, memory_bank):
        self.memory_bank = memory_bank
        self.running = True
        
    def start(self):
        def run():
            while self.running:
                # Apply memory decay every hour
                self.memory_bank.apply_decay()
                time.sleep(3600)
                
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        
    def stop(self):
        self.running = False