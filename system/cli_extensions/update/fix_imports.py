# fix_imports.py
import os

def create_init_files():
    # Create __init__.py in required directories
    directories = [
        'core',
        'core/cognitive_engine',
        'config',
        'interface'
    ]
    
    for dir in directories:
        init_path = os.path.join(dir, '__init__.py')
        if not os.path.exists(init_path):
            with open(init_path, 'w') as f:
                f.write("# Package initialization\n")
            print(f"Created: {init_path}")

if __name__ == "__main__":
    create_init_files()
    print("✅ Import fixes applied. Run your test again.")