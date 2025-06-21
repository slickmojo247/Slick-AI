import csv
import os
import shutil

def parse_csv(csv_path):
    entries = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append({
                "Path": row.get('Path', ''),
                "Filename": row.get('Filename', ''),
                "Content": row.get('Content', '')
            })
    return entries

def rebuild_project(csv_files, output_dir="slick_project"):
    # Clear existing directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    all_entries = []
    for csv_path in csv_files:
        all_entries.extend(parse_csv(csv_path))

    for entry in all_entries:
        path = entry['Path']
        filename = entry['Filename']
        content = entry['Content']

        # Build paths
        path_for_join = path if path else ""
        filename_for_join = filename if filename else ""
        full_path = os.path.join(output_dir, path_for_join, filename_for_join)
        dir_path = os.path.dirname(full_path)

        # Ensure directory exists
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        # Write content if it's a file
        if content and filename:
            with open(full_path, 'w', encoding='utf-8') as f_out:
                if content.startswith('"""') and content.endswith('"""'):
                    content = content[3:-3]
                f_out.write(content)
            print(f"Created: {full_path}")

    print("\n✅ Project structure rebuilt successfully!")

if __name__ == "__main__":
    # These are your project CSVs
    csv_sources = [
        "project_structure.csv",
        "chatgpt.csv"
    ]
    rebuild_project(csv_sources)
