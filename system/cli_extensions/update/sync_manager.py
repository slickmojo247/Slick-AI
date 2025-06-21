# system/sync_manager.py
import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .conflict_resolver import ConflictResolver
from .version_manager import VersionManager

class SyncHandler(FileSystemEventHandler):
    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint
        self.resolver = ConflictResolver()
        self.version_manager = VersionManager()
        self.pending_changes = {}
    
    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            print(f"Detected change: {file_path}")
            
            # Create backup before any sync operations
            backup_path = self.version_manager.create_backup(file_path, "vscode")
            
            # Add to pending changes (debounce rapid saves)
            self.pending_changes[file_path] = time.time()
    
    def process_pending_changes(self):
        """Process changes after debounce period"""
        current_time = time.time()
        for file_path, timestamp in list(self.pending_changes.items()):
            if current_time - timestamp > 2.0:  # 2-second debounce
                self.sync_file(file_path)
                del self.pending_changes[file_path]
    
    def sync_file(self, file_path):
        """Sync file to web interface"""
        with open(file_path, "r") as f:
            content = f.read()
        
        rel_path = str(Path(file_path).relative_to(self.version_manager.project_root))
        payload = {
            "path": rel_path,
            "content": content,
            "source": "vscode",
            "timestamp": time.time()
        }
        
        try:
            response = requests.post(
                f"{self.api_endpoint}/sync",
                json=payload,
                headers={"X-API-KEY": "vscode-secret-key"}
            )
            
            if response.status_code == 409:
                self.handle_conflict(file_path, response.json())
        except Exception as e:
            print(f"Sync failed: {str(e)}")

    def handle_conflict(self, file_path, conflict_data):
        """Resolve conflicts between versions"""
        print(f"Conflict detected in {file_path}")
        
        # Get diff report
        diff_report = self.resolver.generate_diff_report(
            file_path, 
            conflict_data["remote_content"]
        )
        
        # Present options to user
        print("Conflict resolution needed:")
        print(diff_report)
        
        # In actual implementation, this would show in UI
        resolution = self.resolver.manual_merge_ui(diff_report)
        
        # For CLI version, prompt for input
        choice = input("Choose resolution [L]ocal/[R]emote/[A]uto/[M]anual: ").lower()
        
        if choice == "l":
            # Keep local version - do nothing
            print("Keeping local version")
        elif choice == "r":
            # Use remote version
            with open(file_path, "w") as f:
                f.write(conflict_data["remote_content"])
            print("Using remote version")
        elif choice == "a":
            # Attempt auto-merge
            merged_content = self.resolver.auto_merge(file_path, conflict_data["remote_content"])
            with open(file_path, "w") as f:
                f.write(merged_content)
            print("Auto-merge completed")
        elif choice == "m":
            # Open manual editor
            print("Please resolve conflicts manually")
            # In VSCode, this would open the diff editor
        else:
            print("Invalid choice, keeping local version")

def start_sync(api_endpoint="http://localhost:8000"):
    event_handler = SyncHandler(api_endpoint)
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()
    
    try:
        while True:
            event_handler.process_pending_changes()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()