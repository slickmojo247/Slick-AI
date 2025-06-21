import argparse
import logging
import sys
from pathlib import Path
from typing import List
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from your AI!"}


# Platform-specific import inside main function to avoid circular imports
def import_platform_tools():
    if sys.platform == 'win32':
        from app.systems.windows.windows_tools import WindowsTools
        return WindowsTools, None
    else:
        from app.systems.linux.linux_tools import LinuxTools as PlatformTools
        from app.systems.sync_core.sync_core import SyncCore, FileConflictStrategy
        return PlatformTools, SyncCore, FileConflictStrategy

class FormatConverter:
    def __init__(self):
        self.logger = logging.getLogger('format_converter')
        
        # Dynamically import platform tools to avoid circular import
        self.tools, sync_core, FileConflictStrategy = import_platform_tools()
        
        # If we are on a Linux platform, we need to also initialize SyncCore
        if sync_core:
            self.sync = sync_core()
            self.FileConflictStrategy = FileConflictStrategy
        else:
            self.sync = None
            self.FileConflictStrategy = None
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def convert_directory(self, source_dir: str, target_dir: str, 
                         target_os: str, conflict_strategy: str) -> bool:
        """Convert all files in directory to target OS format"""
        if not self.FileConflictStrategy:
            raise RuntimeError("FileConflictStrategy not available on this platform.")
        
        # Map conflict strategy to FileConflictStrategy enum
        strategy_map = {
            'source': self.FileConflictStrategy.PRESERVE_SOURCE,
            'target': self.FileConflictStrategy.PRESERVE_TARGET,
            'newer': self.FileConflictStrategy.PRESERVE_NEWER,
            'merge': self.FileConflictStrategy.MERGE
        }

        try:
            source_path = Path(source_dir)
            target_path = Path(target_dir)
            
            if not source_path.exists():
                self.logger.error(f"Source directory does not exist: {source_dir}")
                return False
                
            if not target_path.exists():
                target_path.mkdir(parents=True)
                self.logger.info(f"Created target directory: {target_dir}")
            
            success = True
            for item in source_path.rglob('*'):
                if item.is_file():
                    rel_path = item.relative_to(source_path)
                    target_file = target_path / rel_path
                    
                    # Ensure target directory exists
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Compare files
                    comparison = self.sync.compare_files(str(item), str(target_file))
                    actions = self.sync.determine_actions(comparison, strategy_map[conflict_strategy])
                    
                    if not actions:  # No action needed
                        continue
                        
                    if 'copy_source_to_target' in actions or 'merge_files' in actions:
                        self.logger.info(f"Converting: {rel_path}")
                        if not self.sync.convert_file(
                            str(item),
                            str(target_file),
                            line_endings=target_os,
                            path_style=target_os
                        ):
                            success = False
                            self.logger.error(f"Failed to convert: {rel_path}")
            
            return success
        except Exception as e:
            self.logger.error(f"Directory conversion failed: {e}")
            return False

    def convert_single_file(self, source_file: str, target_file: str, 
                           target_os: str) -> bool:
        """Convert a single file to target OS format"""
        try:
            self.logger.info(f"Converting file: {source_file}")
            return self.sync.convert_file(
                source_file,
                target_file,
                line_endings=target_os,
                path_style=target_os
            )
        except Exception as e:
            self.logger.error(f"File conversion failed: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description="Convert files between Windows and Linux formats"
    )
    parser.add_argument(
        'source',
        help="Source file or directory"
    )
    parser.add_argument(
        'target',
        help="Target file or directory"
    )
    parser.add_argument(
        '--to',
        choices=['windows', 'linux'],
        required=True,
        help="Target OS format"
    )
    parser.add_argument(
        '--conflict',
        choices=['source', 'target', 'newer', 'merge'],
        default='newer',
        help="Conflict resolution strategy"
    )
    
    args = parser.parse_args()
    
    converter = FormatConverter()
    
    if Path(args.source).is_file():
        success = converter.convert_single_file(
            args.source,
            args.target,
            args.to
        )
    else:
        success = converter.convert_directory(
            args.source,
            args.target,
            args.to,
            args.conflict
        )
    
    if not success:
        print("Conversion completed with errors", file=sys.stderr)
        sys.exit(1)
    
    print("Conversion completed successfully")
    sys.exit(0)

if __name__ == "__main__":
    main()
