import glob
import pandas as pd
from packaging import version

VERSION_MAP = {
    'memory_core.py': ('1.7', '2.1'),
    'cognitive_engine.py': ('1.3', '2.0'),
    'cosmic.css': ('1.3', '1.4')
}

def check_versions():
    for file, (current, target) in VERSION_MAP.items():
        try:
            with open(file) as f:
                content = f.read()
                if f"version {current}" in content:
                    print(f"UPDATE NEEDED: {file} ({current} → {target})")
        except FileNotFoundError:
            print(f"MISSING FILE: {file}")

if __name__ == "__main__":
    check_versions()
