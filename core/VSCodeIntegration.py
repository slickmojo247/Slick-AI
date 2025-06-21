import json
import subprocess
from pathlib import Path

class VSCodeTerminalManager:
    def __init__(self):
        self.workspace = None
        self.terminal_id = None
        self.prompt = 'SLICK> '  # Add this line

    def configure(self, workspace, on_file_change=None, on_terminal_ready=None):
        self.workspace = Path(workspace)
        self._setup_file_watcher(on_file_change)
        self.terminal_id = self._create_terminal()
        if on_terminal_ready:
            on_terminal_ready()

    def send_to_terminal(self, message):
        """Send output to VSCode terminal"""
        print(f"\n[VSCode] {message}\n{self.prompt}", end='', flush=True)


    def _setup_file_watcher(self, callback):
        """Watch for file changes using VSCode API"""
        # Implementation depends on VSCode extension API
        pass

    def _create_terminal(self):
        """Create dedicated terminal instance"""
        try:
            result = subprocess.run(
                ["code", "--new-terminal"],
                cwd=self.workspace,
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except FileNotFoundError:
            return None

    def show_response(self, response):
        """Display formatted AI response"""
        self.send_to_terminal(f"AI Response:\n{'-'*40}\n{response}\n{'-'*40}")

    def update_status(self, status):
        """Update VSCode status bar"""
        print(f"\x1b]1337;SetBadgeFormat={status}\x07", end='')

    def cleanup(self):
        """Clean up terminal resources"""
        if self.terminal_id:
            subprocess.run(["code", "--close-terminal", self.terminal_id])

    def send_to_terminal(self, message):
        try:
            print(f"\n[VSCode] {message}\n{self.prompt}", end='', flush=True)
        except Exception as e:
            print(f"\nTerminal communication error: {str(e)}")
    # Additional VSCode-specific methods...