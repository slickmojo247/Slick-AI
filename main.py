#!/usr/bin/env python3
"""
SLICK AI v2.2 - VSCode-Optimized CLI
"""

import cmd
import sys
import os
from pathlib import Path
from core.Slick_AI_Command_Interface import CommandHandler
from core.VSCodeIntegration import VSCodeTerminalManager

class SlickCLI(cmd.Cmd):
    prompt = 'SLICK> '
    intro = "SLICK AI v2.2 | VSCode Terminal Mode | Type '?' for commands"
    
    def do_alias(self, arg):
        """Execute commands via aliases: alias <name> [args]"""
        parts = arg.split(maxsplit=1)
        alias = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        try:
            result = self.handler.handle_alias(alias, *args)
            if result['success']:
                print(f"Executed '{alias}' → {result['command']}")
                if 'output_path' in result:
                    print(f"Output: {result['output_path']}")
                elif 'output_url' in result:
                    print(f"Available at: {result['output_url']}")
            else:
                print(f"Error: {result['error']}")
        except Exception as e:
            print(f"Alias error: {str(e)}")

    def complete_alias(self, text, line, begidx, endidx):
        return [a for a in self.handler.ALIASES if a.startswith(text)]

    def __init__(self):
        super().__init__()
        self.handler = CommandHandler()
        self.vscode = VSCodeTerminalManager()
        self.active_mode = "technical"  # Default for dev environment
        self.workspace_root = self._detect_workspace()
        
        # VSCode-specific setup
        self._setup_vscode_hooks()
        print(f"Workspace: {self.workspace_root}")

    def _detect_workspace(self):
        """Auto-detect VSCode workspace root"""
        cwd = Path.cwd()
        while cwd != cwd.parent:
            if (cwd / ".vscode").exists():
                return cwd
            cwd = cwd.parent
        return Path.cwd()

    def _setup_vscode_hooks(self):
        """Initialize VSCode-specific integrations"""
        self.vscode.configure(
            workspace=self.workspace_root,
            on_file_change=self._handle_file_change,
            on_terminal_ready=self._send_greeting
        )

    def _handle_file_change(self, file_path):
        """Auto-trigger actions when files change"""
        if file_path.suffix == '.csv':
            self.handler.inject_csv_data(file_path)
        elif file_path.suffix == '.py':
            self.handler.validate_file(file_path)

    def _send_greeting(self):
        """Send welcome message to VSCode terminal"""
        greeting = (
            f"SLICK AI v2.2 connected to {self.workspace_root.name}\n"
            f"Active mode: {self.active_mode} | Projects: "
            f"{len(list(self.workspace_root.glob('*.py')))} Python files"
        )
        self.vscode.send_to_terminal(greeting)

    def do_query(self, arg):
        """Process natural language queries: query <question>"""
        response = self.handler.process_query(arg, self.active_mode)
        self.vscode.show_response(response)

    def do_vscode(self, arg):
        """VSCode-specific commands: vscode <open|run|debug> <target>"""
        args = arg.split()
        if len(args) < 1:
            print("Usage: vscode <open|run|debug> <target>")
            return
            
        cmd, *target = args
        if cmd == "open":
            self.vscode.open_file(Path(target[0]) if target else None)
        elif cmd == "run":
            self.vscode.execute_in_terminal(' '.join(target))
        elif cmd == "debug":
            self.vscode.start_debug_session(target[0] if target else "default")
        else:
            print(f"Unknown vscode command: {cmd}")

    def do_mode(self, arg):
        """Switch AI mode: mode <balanced|technical|creative|homer>"""
        super().do_mode(arg)
        self.vscode.update_status(f"Mode: {self.active_mode}")

    def do_think(self, arg):
        """Store ThinkSession with VSCode integration: think <text>"""
        session_id = self.handler.store_think_session(arg)
        self.vscode.create_comment(
            file_path=self.workspace_root / "think_logs.md",
            content=f"## {session_id}\n{arg}"
        )

    def do_inject(self, arg):
        """Enhanced CSV injection with VSCode awareness: inject <file.csv>"""
        target = Path(arg)
        if not target.is_absolute():
            target = self.workspace_root / target
        self.handler.inject_csv_data(target)
        self.vscode.send_to_terminal(f"Injected {target.name}")

    def do_validate(self, arg):
        """Run validation with VSCode problem matcher: validate [target]"""
        results = self.handler.run_validation(arg or self.workspace_root)
        for error in results.get('errors', []):
            self.vscode.add_problem(
                file=error['file'],
                line=error.get('line', 0),
                message=error['message']
            )

    def precmd(self, line):
        """Hook executed before every command"""
        self.vscode.log_command(line)
        return line

    def postcmd(self, stop, line):
        """Hook executed after every command"""
        self.vscode.update_status(f"Ready | Last: {line.split()[0] if line else 'None'}")
        return stop

    def do_exit(self, arg):
        """Exit with VSCode cleanup: exit"""
        self.vscode.cleanup()
        super().do_exit(arg)

if __name__ == "__main__":
    cli = SlickCLI()
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        cli.vscode.send_to_terminal("\nSLICK AI session terminated safely")
        sys.exit(0)

def do_alias(self, arg):
    """Execute commands via aliases: alias <name> [args]"""
    parts = arg.split(maxsplit=1)
    alias = parts[0]
    args = parts[1:] if len(parts) > 1 else []
    
    try:
        result = self.handler.handle_alias(alias, *args)
        if result['success']:
            print(f"Executed '{alias}' → {result['command']}")
            if 'output_path' in result:
                print(f"Output: {result['output_path']}")
            elif 'output_url' in result:
                print(f"Available at: {result['output_url']}")
        else:
            print(f"Error: {result['error']}")
    except Exception as e:
        print(f"Alias error: {str(e)}")

def complete_alias(self, text, line, begidx, endidx):
    return [a for a in self.handler.ALIASES if a.startswith(text)]   