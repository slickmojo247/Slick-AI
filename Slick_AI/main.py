import cmd
import sys
from core.Slick_AI_Command_Interface import CommandHandler

class SlickCLI(cmd.Cmd):
    prompt = 'SlickAI> '
    intro = "Slick AI System v2.1 | Type 'help' for commands"
    
    def __init__(self):
        super().__init__()
        self.handler = CommandHandler()
        self.active_mode = "balanced"
    
    # Command implementations here (shortened for brevity)
    # Full version includes all do_* methods from previous implementation

if __name__ == "__main__":
    cli = SlickCLI()
    cli.cmdloop()
