import os
from pathlib import Path
from connectors.deepseek import DeepSeekConnector

def try_sync_pending():
    pending_dir = Path(__file__).parent.parent / "sessions" / "local_sync"
    connector = DeepSeekConnector()
    
    for pending_file in pending_dir.glob('*.json'):
        print(f"Attempting to sync: {pending_file.name}")
        result = connector.sync_session(str(pending_file))
        
        if result.get('status') == 'synced':
            pending_file.unlink()
            print(f"✅ Successfully synced {pending_file.name}")
        else:
            print(f"❌ Failed to sync: {result.get('message', 'Unknown error')}")

if __name__ == "__main__":
    print("=== Manual Sync Trigger ===")
    try_sync_pending()
