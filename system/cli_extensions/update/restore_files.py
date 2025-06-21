import csv
import os

def restore_files_from_csv(csv_files, base_dir="slick_ai_system"):
    for csv_file in csv_files:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                path = row.get('Path', '').strip()
                filename = row.get('Filename', '').strip()
                content = row.get('Content', '')

                if not filename:  # Skip if it's a directory or missing
                    continue

                target_dir = os.path.join(base_dir, path)
                target_path = os.path.join(target_dir, filename)

                os.makedirs(target_dir, exist_ok=True)

                # If it's a script, strip triple quotes from content if present
                if content.startswith('"""') and content.endswith('"""'):
                    content = content[3:-3]

                with open(target_path, 'w', encoding='utf-8') as f_out:
                    f_out.write(content)

                print(f"Restored: {target_path}")

    print("\n✅ All files restored successfully.")

if __name__ == "__main__":
    restore_files_from_csv(["project_structure.csv", "chatgpt.csv"])
