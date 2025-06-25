import json
import shutil
from pathlib import Path
import csv
from datetime import datetime

class SmartTransfer:
    def __init__(self):
        self.filters = self._load_filters()
        self.log_file = Path("data/transfer_log.csv")
        self._init_log()

    def _load_filters(self):
        config_path = Path("config/file_filters.json")
        with open(config_path) as f:
            return json.load(f)

    def _init_log(self):
        if not self.log_file.parent.exists():
            self.log_file.parent.mkdir()
        if not self.log_file.exists():
            with open(self.log_file, 'w') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'source', 'destination', 
                    'file_type', 'action', 'size_kb'
                ])

    def _should_transfer(self, path):
        # Check exclude patterns first
        if any(path.match(pattern) for pattern in self.filters["exclude_patterns"]):
            return False

        # Check included extensions
        if path.suffix in self.filters["include_extensions"]:
            return True

        # Check specifically included files
        if path.name in self.filters["include_files"]:
            return True

        # Check directory inclusion
        for dir_pattern in self.filters["include_dirs"]:
            if str(path).startswith(dir_pattern):
                return True

        return False

    def _log_transfer(self, source, dest, action):
        size = source.stat().st_size / 1024  # KB
        with open(self.log_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                str(source),
                str(dest),
                source.suffix,
                action,
                round(size, 2)
            ])

    def transfer_project(self, source_dir, dest_dir):
        source = Path(source_dir)
        dest = Path(dest_dir)
        transferred = 0
        skipped = 0

        for item in source.rglob('*'):
            if not self._should_transfer(item.relative_to(source)):
                skipped += 1
                continue

            rel_path = item.relative_to(source)
            target_path = dest / rel_path

            if item.is_file():
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target_path)
                self._log_transfer(item, target_path, "copied")
                transferred += 1

        print(f"Transfer complete: {transferred} files copied, {skipped} files excluded")
        return transferred