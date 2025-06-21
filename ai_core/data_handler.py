import csv
import json
from pathlib import Path
from typing import Union, Dict, List

class DataHandler:
    def __init__(self):
        self.supported_formats = ['json', 'csv']

    def read(self, file_path: str) -> Union[Dict, List]:
        """Read data from file"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if path.suffix == '.json':
            return self._read_json(path)
        elif path.suffix == '.csv':
            return self._read_csv(path)
        else:
            raise ValueError(f"Unsupported format: {path.suffix}")

    def _read_json(self, path: Path) -> Dict:
        with open(path) as f:
            return json.load(f)

    def _read_csv(self, path: Path) -> List[Dict]:
        with open(path) as f:
            return list(csv.DictReader(f))

    def write(self, data: Union[Dict, List], file_path: str):
        """Write data to file"""
        path = Path(file_path)
        path.parent.mkdir(exist_ok=True)

        if path.suffix == '.json':
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
        elif path.suffix == '.csv':
            with open(path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        else:
            raise ValueError(f"Unsupported format: {path.suffix}")
