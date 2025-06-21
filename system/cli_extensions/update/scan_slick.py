import os

def scan_slick_dir(slick_dir):
    for root,dirs,files in os.walk(slick_dir):
        level = root.replace(slick_dir,'').count(os.path.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        for f in files:
            print(f"{indent}    {f}")

if __name__ == "__main__":
    slick_dir = os.path.join(os.path.dirname(__file__), "slick")
    if os.path.exists(slick_dir):
        print(f"Scanning directory: {slick_dir}")
        scan_slick_dir(slick_dir)
    else:
        print("Error: slick directory not found.")
