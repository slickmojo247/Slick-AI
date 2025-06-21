# File: rescan_and_verify.py
import json
from project_analyzer import analyze_project, export_report
from version_tracker import VersionTracker

def rescan_and_verify(base_version_tag, new_version_tag):
    tracker = VersionTracker()
    
    # Get previous state
    prev_report = load_version_report(base_version_tag)
    
    # Generate new state
    new_analysis = analyze_project()
    new_report = export_report(new_analysis, 'json')
    
    # Save new report
    report_path = f"project_analysis_{new_version_tag}.json"
    with open(report_path, 'w') as f:
        f.write(new_report)
    
    # Compare results
    changes = {
        'duplicates_removed': len(prev_report['duplicate_modules']) - len(new_analysis['duplicate_modules']),
        'orphans_resolved': len(prev_report['potential_orphans']) - len(new_analysis['potential_orphans'])
    }
    
    # Record verification
    tracker.record_action(
        action="rescan_verify",
        files=[report_path],
        tag=new_version_tag,
        backup_path=f"Compared with {base_version_tag}"
    )
    
    return changes

def load_version_report(tag):
    # Implementation to load report from backup
    pass