import csv
import os

SOURCE_MANIFEST = "project_manifest.csv"
TARGET_MANIFEST = "slick_ai_extraction.csv"

# Only include these core folders and files
WHITELIST_KEYWORDS = [
    'slick_ai',
    'private_ai/slick_ai',
    'command_system',
    'ai_system',
    'app.py',
    'prepare_slick_ai_system.py',
    'Galactic_Generation_Explorer.html',
    'style.css',
    'slick_env_config.csv',
    'galactic_html',
    'config',
    'env',
    'static'
]

def detect_type(filename):
    ext = os.path.splitext(filename)[-1].lower()
    if ext == ".py":
        return "py"
    elif ext == ".html":
        return "html"
    elif ext == ".css":
        return "css"
    elif ext == ".js":
        return "js"
    elif ext == ".csv":
        return "csv"
    elif ext == ".json":
        return "json"
    else:
        return "txt"

def should_include(path):
    return any(keyword in path.lower() for keyword in WHITELIST_KEYWORDS)

def extract_minimal_manifest():
    extracted = []
    with open(SOURCE_MANIFEST, newline='', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            rel_path = row.get("Relative Path", "").strip()
            if not rel_path or not should_include(rel_path):
                continue
            folder, filename = os.path.split(rel_path)
            filetype = detect_type(filename)
            extracted.append({
                "folder": folder,
                "filename": filename,
                "type": filetype,
                "logic": ""  # You can fill this later
            })

    with open(TARGET_MANIFEST, "w", newline='', encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["folder", "filename", "type", "logic"])
        writer.writeheader()
        writer.writerows(extracted)

    print(f"✅ Extracted {len(extracted)} Slick AI & Explorer files to: {TARGET_MANIFEST}")

if __name__ == "__main__":
    extract_minimal_manifest()
