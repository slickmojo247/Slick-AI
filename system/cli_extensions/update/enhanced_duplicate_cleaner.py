# File: enhanced_duplicate_cleaner.py
import os
import shutil
import logging
from pathlib import Path
from typing import Dict, List
from version_tracker import VersionTracker
from remove_duplicates import DuplicateCleaner  # Original class

# Configure logging (same as in original)
logger = logging.getLogger(__name__)

class EnhancedDuplicateCleaner(DuplicateCleaner):
    def __init__(self, backup_root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.backup_root = Path(backup_root)
        self.tracker = VersionTracker()
        self.version_tag = ""
    
    def set_version_tag(self, tag):
        """Set a version tag for this cleanup session"""
        self.version_tag = tag
    
    def backup_file(self, file_path: Path) -> Path:
        """
        Enhanced backup that organizes files by version tag
        Returns the backup path if successful, None otherwise
        """
        try:
            # Create versioned backup path
            relative_path = file_path.relative_to(Path.cwd())
            backup_path = self.backup_root / self.version_tag / relative_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            shutil.copy2(file_path, backup_path)
            logger.info(f"Backed up {file_path} to {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Backup failed for {file_path}: {str(e)}")
            return None
    
    def process_recommendations(self, recommendations: Dict[str, List[str]]) -> None:
        """Process recommendations with version tracking"""
        backed_up_files = []
        
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
                    
                # Backup before removal
                backup_path = self.backup_file(remove_path_obj)
                if backup_path:
                    backed_up_files.append(str(backup_path))
                
                # Perform removal
                self.remove_file(remove_path_obj)
        
        # Record this version
        version_id = self.tracker.record_action(
            action="duplicate_cleanup",
            files=list(recommendations.keys()),
            backup_path=str(self.backup_root / self.version_tag),
            tag=self.version_tag
        )
        logger.info(f"Recorded cleanup as version {version_id} with tag '{self.version_tag}'")

if __name__ == "__main__":
    import argparse
    from datetime import datetime
    
    parser = argparse.ArgumentParser(description='Enhanced duplicate file cleaner with version tracking')
    parser.add_argument('analysis_file', help='Path to project analysis markdown file')
    parser.add_argument('--backup-root', default='backups', help='Root directory for backups')
    parser.add_argument('--tag', help='Custom version tag (defaults to timestamp)')
    parser.add_argument('--execute', action='store_false', dest='dry_run',
                       help='Actually delete files (default is dry run)')
    
    args = parser.parse_args()
    
    # Initialize cleaner
    cleaner = EnhancedDuplicateCleaner(
        backup_root=args.backup_root,
        dry_run=args.dry_run,
        backup=True
    )
    
    # Set version tag
    version_tag = args.tag if args.tag else datetime.now().strftime("v%Y%m%d_%H%M%S")
    cleaner.set_version_tag(version_tag)
    
    logger.info(f"Starting duplicate cleanup (version: {version_tag})")
    if cleaner.dry_run:
        logger.info("Running in DRY RUN mode - no files will be deleted")
    
    try:
        recommendations = cleaner.parse_recommendations(args.analysis_file)
        if not recommendations:
            logger.warning("No duplicate file recommendations found")
            exit(0)
            
        logger.info(f"Found {len(recommendations)} duplicate groups to process")
        cleaner.process_recommendations(recommendations)
        cleaner.save_report()
        
        logger.info("Cleanup complete!")
        if cleaner.dry_run:
            logger.info("Run with --execute to perform actual deletions")
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")
        exit(1)