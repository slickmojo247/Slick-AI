#!/usr/bin/env python3
"""
Project Structure Analyzer and Consolidation Advisor
"""
import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Configuration
CRITICAL_ROOT_FILES = {
    'main.py', 'app.py', 'start.py', 'run.py', 
    'requirements.txt', 'setup.py', 'manage.py'
}
IGNORE_DIRS = {'.git', '__pycache__', 'venv', '.idea', 'node_modules'}
PYTHON_FILE_PATTERN = re.compile(r'^[a-zA-Z].*\.py$')

def analyze_project(root_path: str = '.') -> Dict:
    """Generate a detailed project structure report"""
    analysis = {
        'root_files': [],
        'potential_orphans': [],
        'duplicate_modules': {},
        'structure': {},
        'recommendations': []
    }
    
    # Track module bases for duplicates
    module_bases: Dict[str, List[str]] = {}
    
    for root, dirs, files in os.walk(root_path):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        rel_path = os.path.relpath(root, root_path)
        current_level = analysis['structure']
        
        if rel_path != '.':
            for part in rel_path.split(os.sep):
                current_level = current_level.setdefault(part, {})
        
        for file in files:
            file_path = Path(root) / file
            rel_file_path = str(file_path.relative_to(root_path))
            
            # Check if Python file
            is_python = file.endswith('.py')
            
            # Root level analysis
            if root == root_path:
                if is_python and file not in CRITICAL_ROOT_FILES:
                    analysis['potential_orphans'].append(rel_file_path)
                elif is_python:
                    analysis['root_files'].append(rel_file_path)
            
            # Module duplicate detection
            if is_python:
                base_name = file.split('.')[0]
                module_bases.setdefault(base_name, []).append(rel_file_path)
                
            current_level[file] = {
                'type': 'python' if is_python else 'file',
                'size': os.path.getsize(file_path)
            }
    
    # Identify duplicate modules
    analysis['duplicate_modules'] = {
        base: paths for base, paths in module_bases.items() 
        if len(paths) > 1 and not base.startswith('test_')
    }
    
    # Generate recommendations
    generate_recommendations(analysis)
    
    return analysis

def generate_recommendations(analysis: Dict):
    """Generate actionable consolidation recommendations"""
    recs = []
    
    # Orphaned files recommendation
    if analysis['potential_orphans']:
        recs.append({
            'action': 'move',
            'files': analysis['potential_orphans'],
            'suggested_location': 'core/utils/',
            'reason': 'Loose Python files should be organized into modules'
        })
    
    # Duplicate modules recommendation
    for module, paths in analysis['duplicate_modules'].items():
        newest = max(paths, key=lambda p: os.path.getmtime(p))
        old_files = [p for p in paths if p != newest]
        
        recs.append({
            'action': 'consolidate',
            'keep': newest,
            'remove': old_files,
            'reason': f'Duplicate {module} implementations found'
        })
    
    # Structure optimization
    top_level_dirs = set(analysis['structure'].keys())
    ideal_structure = {'core', 'interfaces', 'services', 'tests'}
    
    missing_dirs = ideal_structure - top_level_dirs
    if missing_dirs:
        recs.append({
            'action': 'create',
            'directories': list(missing_dirs),
            'reason': 'Standard project structure not fully implemented'
        })
    
    analysis['recommendations'] = recs

def export_report(analysis: Dict, format: str = 'markdown'):
    """Export analysis report in specified format"""
    report = []
    
    if format == 'markdown':
        report.append("# Project Structure Analysis Report\n")
        
        # Summary
        report.append("## Summary\n")
        report.append(f"- Root files: {len(analysis['root_files']}")
        report.append(f"- Potential orphans: {len(analysis['potential_orphans'])}")
        report.append(f"- Duplicate modules: {len(analysis['duplicate_modules'])}\n")
        
        # Recommendations
        report.append("## Recommendations\n")
        for rec in analysis['recommendations']:
            report.append(f"### {rec['action'].title()} {rec.get('directories', rec.get('files', [''])[0]}")
            report.append(f"**Reason:** {rec['reason']}")
            
            if rec['action'] == 'move':
                report.append(f"**Files to move:**\n```\n" + "\n".join(rec['files']) + "\n```")
                report.append(f"**Suggested location:** `{rec['suggested_location']}`")
            elif rec['action'] == 'consolidate':
                report.append(f"**Keep:** `{rec['keep']}`")
                report.append(f"**Remove:**\n```\n" + "\n".join(rec['remove']) + "\n```")
            elif rec['action'] == 'create':
                report.append(f"**Directories to create:**\n```\n" + "\n".join(rec['directories']) + "\n```")
            
            report.append("")
        
        # Structure tree
        report.append("## Current Structure\n```")
        report.append(print_structure(analysis['structure']))
        report.append("```")
        
        return "\n".join(report)
    else:
        return json.dumps(analysis, indent=2)

def print_structure(structure: Dict, level: int = 0) -> str:
    """Generate ASCII structure tree"""
    lines = []
    indent = "    " * level
    
    for name, contents in structure.items():
        if isinstance(contents, dict):
            lines.append(f"{indent}├── {name}/")
            lines.append(print_structure(contents, level + 1))
        else:
            lines.append(f"{indent}├── {name}")
    
    return "\n".join(lines)

if __name__ == "__main__":
    print("Analyzing project structure...")
    analysis = analyze_project()
    
    # Save reports
    with open("project_analysis.md", "w") as f:
        f.write(export_report(analysis, 'markdown'))
    
    with open("project_analysis.json", "w") as f:
        f.write(export_report(analysis, 'json'))
    
    print("Analysis complete!")
    print(f"- Markdown report saved to project_analysis.md")
    print(f"- JSON report saved to project_analysis.json")
    print("\nKey recommendations:")
    
    for i, rec in enumerate(analysis['recommendations'][:3], 1):
        print(f"{i}. {rec['action'].title()} {rec.get('directories', rec.get('files', [''])[0]}")
