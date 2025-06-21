# Run FIRST after reset
from pathlib import Path
import json
import sqlite3

def restore_from_snapshot(snapshot_dir="snapshots/latest"):
    # 1. Rebuild file structure
    with open(f"{snapshot_dir}/manifest.json") as f:
        manifest = json.load(f)
    
    # 2. Restore files
    for file in manifest['files']:
        Path(file['path']).parent.mkdir(exist_ok=True)
        with open(file['path'], 'w') as f:
            f.write(file['content'])  # Content stored in delta format
    
    # 3. Rebuild databases
    for db, schema in manifest['databases'].items():
        conn = sqlite3.connect(db)
        conn.executescript(schema)
        conn.close()

    print(f"System restored from {snapshot_dir}")

# Example usage:
# restore_from_snapshot("snapshots/delta_20240615_143000")