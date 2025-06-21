import csv
import os

INPUT_MANIFEST = "project_manifest.csv"
OUTPUT_MANIFEST = "code_ready_manifest.csv"

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
    else:
        return "txt"

def convert_manifest():
    entries = []
    with open(INPUT_MANIFEST, newline='', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            relative_path = row.get("Relative Path", "").strip()
            if not relative_path or relative_path.endswith("/"):
                continue  # Skip folders or blanks

            folder, filename = os.path.split(relative_path)
            filetype = detect_type(filename)
            entries.append({
                "folder": folder,
                "filename": filename,
                "type": filetype,
                "logic": ""  # We'll keep this blank for now
            })

    with open(OUTPUT_MANIFEST, "w", newline='', encoding='utf-8') as outfile:
        fieldnames = ["folder", "filename", "type", "logic"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(entries)

    print(f"✅ Converted {len(entries)} entries to {OUTPUT_MANIFEST}")

if __name__ == "__main__":
    convert_manifest()
