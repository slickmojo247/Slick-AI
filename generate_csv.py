import os
import csv
from pathlib import Path

# === CONFIGURATION ===
excluded_dirs = {"venv", "__pycache__", ".git", "node_modules", "Color_tagged"}
excluded_exts = {".pyc", ".log", ".tmp", ".cache"}

# === MAIN SETUP ===
base_dir = os.getcwd()
project_name = Path(base_dir).name.replace(" ", "_")
csv_filename = f"{project_name}.csv"

file_list = []

for folder_path, subdirs, files in os.walk(base_dir):
    if any(ex in folder_path for ex in excluded_dirs):
        continue
    for file in files:
        ext = Path(file).suffix.lower()
        if ext in excluded_exts:
            continue
        try:
            file_path = os.path.join(folder_path, file)
            stats = os.stat(file_path)
            file_list.append({
                "File Name": file,
                "Extension": ext,
                "Size (KB)": round(stats.st_size / 1024, 2),
                "Last Modified": stats.st_mtime,
                "Relative Path": os.path.relpath(file_path, base_dir),
                "Full Path": file_path
            })
        except Exception:
            continue

if file_list:
    with open(csv_filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=file_list[0].keys())
        writer.writeheader()
        writer.writerows(file_list)
    print(f"✅ CSV created: {csv_filename}")
else:
    print("⚠️ No valid files found.")
