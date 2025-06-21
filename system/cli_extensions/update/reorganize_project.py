import os
import shutil
from pathlib import Path

# Define the new folder structure mapping
FILE_MAPPING = {
    # Core components
    'ai_system.py': 'core/ai_system.py',
    'command_system.py': 'core/command_system.py',
    
    # Configuration
    'slick_env_config.csv': 'config/slick_env_config.csv',
    'commands.csv': 'config/commands.csv',
    
    # Data files
    'memory_nodes.csv': 'data/memory_nodes.csv',
    
    # Memory system
    'memory_node.py': 'memory/memory_node.py',
    
    # Personality
    'character_interactions': 'personality/character_interactions',
    
    # Interface
    'web_interface': 'interface/web_interface',
    'api': 'interface/api',
    
    # Modules
    'modules': 'modules',
    
    # CLI
    'cli.py': 'cli/cli.py',
    'slick_cli.py': 'cli/slick_cli.py',
    
    # Scripts
    'build_project.py': 'scripts/build_project.py',
    'convert_manifest.py': 'scripts/convert_manifest.py',
    'extract_slick_ai_components.py': 'scripts/extract_slick_ai_components.py',
    'move_files.py': 'scripts/move_files.py',
    'prepare_slick_ai_system.py': 'scripts/prepare_slick_ai_system.py',
    'rebuild.py': 'scripts/rebuild.py',
    'Backup.py': 'scripts/Backup.py',
    
    # Projects
    'project_manifest.csv': 'projects/project_manifest.csv',
    'projects_savepoint.csv': 'projects/projects_savepoint.csv',
    'slick_ai_extraction.csv': 'projects/slick_ai_extraction.csv',
    'slick_ai_full_separation.csv': 'projects/slick_ai_full_separation.csv',
    'slick_ai_project.csv': 'projects/slick_ai_project.csv',
    'slick_ai_separation_plan.csv': 'projects/slick_ai_separation_plan.csv',
    
    # Docs
    'README_SLICK_AI.md': 'docs/README_SLICK_AI.md',
    
    # Root files to keep
    'SLICK.py': 'SLICK.py',
    'app.py': 'app.py',
    'requirements.txt': 'requirements.txt',
    'Slick_chatgpt.csv': 'Slick_chatgpt.csv',
    'chatgpt.csv': 'chatgpt.csv',
    'Slick_upgrade.csv': 'Slick_upgrade.csv',
    
    # Directories to move as-is
    'ai_scripts': 'modules/ai_scripts',
    'backups': 'memory/backups',
    'logs': 'system/logs',
}

def move_files_with_structure():
    # Create all target directories first
    for target in set(os.path.dirname(t) for t in FILE_MAPPING.values() if not str(t).endswith('/')):
        if target:  # Only create if path is not empty
            os.makedirs(target, exist_ok=True)
    
    # Process each file/directory
    for source, target in FILE_MAPPING.items():
        source_path = Path(source)
        target_path = Path(target)
        
        if not source_path.exists():
            print(f"⚠️ Warning: Source not found - {source}")
            continue
        
        if source_path.is_dir():
            # Handle directory movement
            print(f"📂 Moving directory: {source} -> {target}")
            try:
                if target_path.exists():
                    # Merge directories if target exists
                    print(f"   🔄 Merging with existing directory: {target}")
                    for item in os.listdir(source_path):
                        src_item = source_path / item
                        tgt_item = target_path / item
                        if tgt_item.exists():
                            print(f"   ⚠️ Conflict: {tgt_item} already exists - skipping")
                        else:
                            shutil.move(str(src_item), str(tgt_item))
                    # Remove now-empty source directory
                    try:
                        source_path.rmdir()
                        print(f"   ✔️ Removed empty source directory: {source}")
                    except OSError as e:
                        print(f"   ❌ Could not remove directory {source}: {e}")
                else:
                    shutil.move(source, target)
                    print(f"   ✔️ Moved successfully")
            except Exception as e:
                print(f"   ❌ Error moving {source}: {e}")
        else:
            # Handle file movement
            print(f"📄 Moving file: {source} -> {target}")
            try:
                if target_path.exists():
                    print(f"   ⚠️ Conflict: {target} already exists - skipping")
                else:
                    shutil.move(source, target)
                    print(f"   ✔️ Moved successfully")
            except Exception as e:
                print(f"   ❌ Error moving {source}: {e}")
    
    # Special handling for __pycache__
    if Path('__pycache__').exists():
        print("\n🔍 Found __pycache__ directory. Recommend:")
        print("   - Delete it with: rm -rf __pycache__")
        print("   - It will be regenerated automatically when needed")

    print("\n✅ Reorganization complete!")
    print("Note: You may need to update import statements in your Python files")
    print("to reflect the new file locations.")

if __name__ == '__main__':
    print("🚀 Starting Slick AI project reorganization...\n")
    print("This will move files to the new structure. Original files will be moved, not copied.\n")
    confirm = input("Do you want to continue? [y/N] ").strip().lower()
    if confirm == 'y':
        move_files_with_structure()
    else:
        print("Operation cancelled")