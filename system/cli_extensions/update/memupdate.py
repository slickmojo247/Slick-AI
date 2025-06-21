import zipfile, os, shutil

def extract_and_merge(zip_path="AutoMemory_Engine.zip", target_dir="."):
    if not os.path.exists(zip_path):
        print("Zip file not found:", zip_path)
        return

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("_temp_update")

    for root, dirs, files in os.walk("_temp_update"):
        for name in files:
            src_path = os.path.join(root, name)
            rel_path = os.path.relpath(src_path, "_temp_update")
            dst_path = os.path.join(target_dir, rel_path)

            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)
            print(f"Updated: {dst_path}")

    shutil.rmtree("_temp_update")
    os.remove(zip_path)
    print("✅ Update complete and zip removed.")

if __name__ == "__main__":
    extract_and_merge()
