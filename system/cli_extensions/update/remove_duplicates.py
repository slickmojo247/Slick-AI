import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import logging
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('duplicate_cleanup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DuplicateCleaner:
    def __init__(self, dry_run: bool = True, backup: bool = False):
        self.dry_run = dry_run
        self.backup = backup
        self.backup_dir = Path('duplicate_backups')
        self.actions = {
            'deleted': [],
            'backed_up': [],
            'skipped': [],
            'errors': []
        }
        
        if self.backup and not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True)
    
    def parse_recommendations(self, analysis_file: str) -> Dict[str, List[str]]:
        """Parse the project analysis file to extract keep/remove recommendations"""
        recommendations = {}
        current_section = None
        keep_path = None
        
        with open(analysis_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Detect recommendation sections
                if line.startswith("### Consolidate"):
                    current_section = "consolidate"
                    continue
                elif line.startswith("### Move"):
                    current_section = "move"
                    continue
                
                # Process consolidate recommendations
                if current_section == "consolidate":
                    if line.startswith("Keep:"):
                        keep_path = line.replace("Keep:", "").strip().strip('`')
                        remove_paths = []
                    elif line.startswith("Remove:"):
                        if keep_path:  # Only process if we have a keep_path
                            remove_path = line.replace("Remove:", "").strip().strip('`')
                            if remove_path:  # Only add if path is not empty
                                remove_paths.append(remove_path)
                    elif line.startswith("```") and keep_path and remove_paths:
                        recommendations[keep_path] = remove_paths
                        keep_path = None
                        remove_paths = []
                        current_section = None
        
        return recommendations
    
    def backup_file(self, file_path: Path) -> bool:
        """Create a backup of the file before deletion"""
        try:
            backup_path = self.backup_dir / file_path.relative_to(Path.cwd())
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, backup_path)
            logger.info(f"Backed up {file_path} to {backup_path}")
            self.actions['backed_up'].append(str(file_path))
            return True
        except Exception as e:
            logger.error(f"Failed to backup {file_path}: {str(e)}")
            self.actions['errors'].append(f"Backup failed for {file_path}: {str(e)}")
            return False
    
    def remove_file(self, file_path: Path) -> bool:
        """Remove a file with checks and optional backup"""
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            self.actions['skipped'].append(str(file_path))
            return False
        
        if file_path.is_dir():
            logger.warning(f"Skipping directory: {file_path}")
            self.actions['skipped'].append(str(file_path))
            return False
        
        if self.backup:
            if not self.backup_file(file_path):
                return False
        
        try:
            if self.dry_run:
                logger.info(f"[DRY RUN] Would delete {file_path}")
                self.actions['deleted'].append(str(file_path))
                return True
            else:
                file_path.unlink()
                logger.info(f"Deleted {file_path}")
                self.actions['deleted'].append(str(file_path))
                return True
        except Exception as e:
            logger.error(f"Failed to delete {file_path}: {str(e)}")
            self.actions['errors'].append(f"Deletion failed for {file_path}: {str(e)}")
            return False
    
    def process_recommendations(self, recommendations: Dict[str, List[str]]) -> None:
        """Process all recommendations to remove duplicates"""
        for keep_path, remove_paths in recommendations.items():
            keep_path_obj = Path(keep_path)
            
            if not keep_path_obj.exists():
                logger.warning(f"Keep file not found: {keep_path}. Skipping related deletions.")
                self.actions['skipped'].extend(remove_paths)
                continue
            
            logger.info(f"Processing duplicates for {keep_path}")
            
            for remove_path in remove_paths:
                remove_path_obj = Path(remove_path)
                if remove_path_obj == Path('.'):  # Skip current directory
                    continue
                self.remove_file(remove_path_obj)
    
    def save_report(self) -> None:
        """Save a report of all actions taken"""
        report_path = Path('duplicate_cleanup_report.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.actions, f, indent=2)
        logger.info(f"Saved action report to {report_path}")

def main():
    parser = argparse.ArgumentParser(description='Remove duplicate files based on project analysis.')
    parser.add_argument('analysis_file', help='Path to the project analysis markdown file')
    parser.add_argument('--execute', action='store_false', dest='dry_run',
                       help='Actually delete files (default is dry run)')
    parser.add_argument('--backup', action='store_true',
                       help='Create backups of files before deletion')
    
    args = parser.parse_args()
    
    cleaner = DuplicateCleaner(dry_run=args.dry_run, backup=args.backup)
    
    logger.info("Starting duplicate file cleanup")
    if cleaner.dry_run:
        logger.info("Running in DRY RUN mode - no files will be deleted")
    
    try:
        recommendations = cleaner.parse_recommendations(args.analysis_file)
        if not recommendations:
            logger.warning("No duplicate file recommendations found in the analysis file")
            return
        
        logger.info(f"Found {len(recommendations)} duplicate file groups to process")
        cleaner.process_recommendations(recommendations)
        cleaner.save_report()
        
        logger.info("Duplicate file cleanup completed")
        if cleaner.dry_run:
            logger.info("Run with --execute to actually perform deletions")
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        cleaner.save_report()

if __name__ == '__main__':
    main()