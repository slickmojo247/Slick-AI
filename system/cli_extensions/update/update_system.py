# scripts/update_system.py (combines memupdate.py and migrate_versions.py)
import os
import zipfile
import shutil
from typing import Dict

class SystemUpdater:
    def __init__(self):
        self.VERSION_MAP = {
            "core": {"2.1.x": "2.2.x"},
            "memory": {"1.5.x": "1.6.x"}
        }

    def extract_and_merge(self, zip_path: str, target_dir: str = ".") -> None:
        """Handles zip file updates from memupdate.py"""
        if not os.path.exists(zip_path):
            raise FileNotFoundError(f"Zip file not found: {zip_path}")

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("_temp_update")

        for root, _, files in os.walk("_temp_update"):
            for name in files:
                src_path = os.path.join(root, name)
                rel_path = os.path.relpath(src_path, "_temp_update")
                dst_path = os.path.join(target_dir, rel_path)
                
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src_path, dst_path)

        shutil.rmtree("_temp_update")
        os.remove(zip_path)

    def migrate_versions(self) -> None:
        """Handles version migrations from migrate_versions.py"""
        for module, versions in self.VERSION_MAP.items():
            current = self._get_current_version(module)
            target = versions.get(current)
            
            if target:
                self._run_migration_script(module, current, target)

    def _get_current_version(self, module: str) -> str:
        """Simplified version detection"""
        return "2.1.x" if module == "core" else "1.5.x"

    def _run_migration_script(self, module: str, from_v: str, to_v: str) -> None:
        """Placeholder for actual migration logic"""
        print(f"Executing {module}/{from_v}_to_{to_v}.py...")
        # Actual implementation would import and run migration scripts