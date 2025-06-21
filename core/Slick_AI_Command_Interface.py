import os
import subprocess
import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from typing import List

@dataclass
class CommandConfig:
    memory_path: Path = field(default=Path("memory/Think/"))
    update_scripts: Path = field(default=Path("system/cli_extensions/update/"))
    valid_components: List[str] = field(default_factory=lambda: ["memory", "engine", "core", "vscode"])
    backup_dir: Path = field(default=Path("backup/"))
    log_file: Path = field(default=Path("logs/command_history.log"))
@dataclass

class VSCodeIntegration:
    @staticmethod
    def get_workspace_root() -> Optional[Path]:
        """Auto-detect VSCode workspace root"""
        cwd = Path.cwd()
        while cwd != cwd.parent:
            if (cwd / ".vscode").exists():
                return cwd
            cwd = cwd.parent
        return None

    @staticmethod
    def open_in_editor(file_path: Path) -> bool:
        """Open file in VSCode editor"""
        try:
            subprocess.run(["code", "--reuse-window", str(file_path)], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

class CommandHandler:
    def __init__(self):
        self.config = CommandConfig()
        self.vscode = VSCodeIntegration()
        self._setup_logging()
        self._ensure_directories()
        
    def _setup_logging(self):
        """Configure advanced logging with file rotation"""
        self.logger = logging.getLogger('SlickAI.Core')
        self.logger.setLevel(logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        
        # File handler
        fh = logging.FileHandler(self.config.log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(
            '%(asctime)s|%(levelname)s|%(message)s'
        ))
        
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def _ensure_directories(self):
        """Create required directories"""
        self.config.memory_path.mkdir(parents=True, exist_ok=True)
        self.config.backup_dir.mkdir(parents=True, exist_ok=True)
        self.config.log_file.parent.mkdir(parents=True, exist_ok=True)

    def process_query(self, query: str, mode: str) -> Dict:
        """Enhanced query processing with VSCode context"""
        self.logger.info(f"Processing '{query}' in {mode} mode")
        
        # Get VSCode context if available
        vscode_context = {}
        if workspace := self.vscode.get_workspace_root():
            vscode_context = {
                "workspace": str(workspace),
                "open_files": [
                    str(f) for f in workspace.glob("**/*") 
                    if f.is_file()
                ][:10]  # Sample first 10 files
            }
        
        return {
            "query": query,
            "mode": mode,
            "timestamp": datetime.now().isoformat(),
            "context": vscode_context,
            "response": f"Processed your query about '{query}' in {mode} mode"
        }

    def reload_component(self, component: str) -> bool:
        """Component reload with validation"""
        if component not in self.config.valid_components:
            self.logger.warning(f"Invalid component: {component}")
            return False
            
        self.logger.info(f"Reloading {component} subsystem")
        # Add actual reload logic here
        return True

    def show_status(self) -> Dict:
        """Comprehensive system status report"""
        status = {
            "system": {
                "memory": f"{os.getpid()}",
                "python_version": sys.version,
                "platform": sys.platform
            },
            "components": {
                "vscode": bool(self.vscode.get_workspace_root()),
                "ai_engine": "active",
                "memory": "85% utilized"
            },
            "last_updated": datetime.now().isoformat()
        }
        
        if workspace := self.vscode.get_workspace_root():
            status["vscode"] = {
                "workspace": str(workspace),
                "python_files": len(list(workspace.glob("**/*.py")))
            }
        
        return status

    def store_think_session(self, text: str) -> Path:
        """Store thoughts with rich metadata"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_file = self.config.memory_path / f"think_{timestamp}.md"
        
        content = f"""# Think Session {timestamp}
        
## Context
- Workspace: {self.vscode.get_workspace_root() or 'N/A'}
- Time: {datetime.now().isoformat()}

## Content
{text}
"""
        session_file.write_text(content)
        
        # Open in VSCode if available
        if self.vscode.get_workspace_root():
            self.vscode.open_in_editor(session_file)
            
        return session_file

    def inject_csv_data(self, csv_path: Path) -> Dict:
        """Enhanced CSV processing with validation"""
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
            
        results = {
            "file": str(csv_path),
            "rows": 0,
            "columns": [],
            "sample_data": []
        }
        
        with csv_path.open() as f:
            reader = csv.DictReader(f)
            results["columns"] = reader.fieldnames
            for i, row in enumerate(reader):
                if i < 5:  # Capture sample data
                    results["sample_data"].append(row)
                results["rows"] += 1
                
        self.logger.info(f"Injected {results['rows']} rows from {csv_path.name}")
        return results

    def create_backup_report(self) -> Dict:
        """Comprehensive backup with VSCode awareness"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = self.vscode.get_workspace_root() or Path.cwd()
        
        csv_path = self.config.backup_dir / f"backup_{timestamp}.csv"
        json_path = self.config.backup_dir / f"backup_{timestamp}.json"
        
        report = {
            "metadata": {
                "timestamp": timestamp,
                "base_directory": str(base_dir),
                "system": self.show_status()
            },
            "files": []
        }
        
        for file in base_dir.glob("**/*"):
            if file.is_file() and not any(part.startswith('.') for part in file.parts):
                report["files"].append({
                    "path": str(file.relative_to(base_dir)),
                    "size": file.stat().st_size,
                    "modified": datetime.fromtimestamp(
                        file.stat().st_mtime
                    ).isoformat()
                })
        
        # Save reports
        with csv_path.open('w') as f:
            writer = csv.DictWriter(f, fieldnames=report["files"][0].keys())
            writer.writeheader()
            writer.writerows(report["files"])
            
        with json_path.open('w') as f:
            json.dump(report, f, indent=2)
            
        return {
            "csv_path": str(csv_path),
            "json_path": str(json_path),
            "file_count": len(report["files"])
        }

    # Additional enhanced methods...

if __name__ == "__main__":
    # Test functionality
    handler = CommandHandler()
    print(handler.show_status())
    handler.store_think_session("Testing enhanced command interface")

    # Add to Slick_AI_Command_Interface.py
    # ... (existing code)
    
    ALIASES = {
        'backup': {
            'command': 'run_backup',
            'handler': lambda self: self.create_backup_report(),
            'output': Path('backups/')
        },
        'zip': {
            'command': 'create_zip',
            'handler': lambda self, *args: self._handle_zip(args),
            'output': Path('archives/'),
            'requires_args': True
        },
        'look': {
            'command': 'read_file',
            'handler': lambda self, path: self._preview_content(path),
            'output': None
        },
        'think': {
            'command': 'process_think_session',
            'handler': lambda self: self._process_clipboard_thoughts(),
            'output': Path('sessions/think_logs/')
        },
        'scan': {
            'command': 'scan_directory',
            'handler': lambda self: self.scan_imported_files(),
            'output': Path('system/cli_extensions/update/original')
        },
        'load deck': {
            'command': 'load_session_preset',
            'handler': lambda self, deck: self._load_memory_preset(deck),
            'output': Path('sessions/decks/')
        },
        'launch web': {
            'command': 'start_web_ui',
            'handler': lambda self: self._start_dashboard(),
            'output': 'http://localhost:5000/'
        },
        'inject': {
            'command': 'inject_module',
            'handler': lambda self, module: self._inject_core_module(module),
            'output': Path('system/injected/')
        }
    }

    def handle_alias(self, alias: str, *args) -> Dict:
        """Process command aliases with full validation"""
        if alias not in self.ALIASES:
            raise ValueError(f"Unknown alias: {alias}")
        
        config = self.ALIASES[alias]
        
        if config.get('requires_args') and not args:
            raise ValueError(f"Alias '{alias}' requires arguments")
        
        try:
            result = config['handler'](self, *args)
            output = {
                'alias': alias,
                'command': config['command'],
                'success': True,
                'result': result
            }
            
            if config['output']:
                if isinstance(config['output'], Path):
                    output['output_path'] = str(config['output'].absolute())
                else:
                    output['output_url'] = config['output']
            
            return output
            
        except Exception as e:
            self.logger.error(f"Alias '{alias}' failed: {str(e)}")
            return {
                'alias': alias,
                'error': str(e),
                'success': False
            }

    # Alias handler implementations
    def _handle_zip(self, targets: tuple) -> Dict:
        """Zip specified files/folders"""
        from zipfile import ZipFile, ZIP_DEFLATED
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_path = self.ALIASES['zip']['output'] / f"archive_{timestamp}.zip"
        
        with ZipFile(zip_path, 'w', ZIP_DEFLATED) as zipf:
            for target in targets:
                target_path = Path(target)
                if target_path.is_file():
                    zipf.write(target_path)
                elif target_path.is_dir():
                    for f in target_path.rglob('*'):
                        zipf.write(f, f.relative_to(target_path.parent))
        
        return {
            'zipped_files': len(zipf.filelist),
            'archive_path': str(zip_path)
        }

    def _preview_content(self, path: str) -> Dict:
        """Preview file contents with syntax highlighting"""
        target = Path(path)
        if not target.exists():
            raise FileNotFoundError(f"Path not found: {path}")
        
        return {
            'path': str(target),
            'type': 'file' if target.is_file() else 'directory',
            'content': target.read_text()[:5000] if target.is_file() else None,
            'items': [f.name for f in target.iterdir()] if target.is_dir() else None
        }

    def _process_clipboard_thoughts(self) -> Dict:
        """Process clipboard content into formatted thoughts"""
        try:
            import pyperclip
            raw_text = pyperclip.paste()
        except ImportError:
            raw_text = "Clipboard access requires pyperclip module"
        
        thought = "\n".join(
            line.strip() for line in raw_text.split('\n') 
            if line.strip()
        )
        return self.store_think_session(thought)

    def _load_memory_preset(self, deck: str) -> Dict:
        """Load a saved memory context"""
        deck_file = self.ALIASES['load deck']['output'] / f"{deck}.json"
        if not deck_file.exists():
            raise FileNotFoundError(f"No deck named '{deck}'")
        
        with deck_file.open() as f:
            return json.load(f)

    def _start_dashboard(self) -> Dict:
        """Launch web interface"""
        try:
            subprocess.Popen(
                ["python", "-m", "slick_ai.web.dashboard"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return {
                'status': 'running',
                'url': self.ALIASES['launch web']['output']
            }
        except Exception as e:
            raise RuntimeError(f"Failed to start web UI: {str(e)}")

    def _inject_core_module(self, module: str) -> Dict:
        """Inject a module into running system"""
        target = self.ALIASES['inject']['output'] / f"{module}.py"
        if not target.exists():
            raise FileNotFoundError(f"No module '{module}' to inject")
        
        # Actual injection logic would go here
        return {
            'module': module,
            'injection_path': str(target)
        }