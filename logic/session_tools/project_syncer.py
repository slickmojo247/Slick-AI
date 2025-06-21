import os
from pathlib import Path
from datetime import datetime
from connectors.local_sync import LocalSyncManager
from connectors.deepseek import DeepSeekConnector

def get_all_sessions(project_root):
    session_dir = Path(project_root) / "sessions"
    return sorted(session_dir.glob('session_*.csv'), key=os.path.getmtime)

def print_status(result):
    icons = {
        'local_saved': '🔵',
        'synced': '🟢',
        'error': '🔴'
    }
    print(f"{icons.get(result['status'], '⚪')} {result['message']}")
    if 'path' in result:
        print(f"   ↳ Location: {result['path']}")

if __name__ == "__main__":
    project_root = str(Path(__file__).parent.parent.parent)
    local_mgr = LocalSyncManager()
    
    print(f"\n{' Session Manager ':=^40}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Process CSV sessions
    sessions = get_all_sessions(project_root)
    if sessions:
        latest = sessions[-1]
        print(f"Processing: {latest.name}")
        
        with open(latest, 'r') as f:
            result = local_mgr.save_session(f.read())
        print_status(result)
    else:
        print("⚠️ No session files found")
    
    # Show pending syncs
    pending = local_mgr.get_pending_sessions()
    print(f"\nPending syncs: {len(pending)}")
    for item in pending[-3:]:
        print(f" - {item.name}")
    
    print("\n" + "="*40)
