from ..cli.commands import *  # Import all commands

class Dispatcher:
    def execute(self, command):
        if command in COMMAND_REGISTRY:  # From CLI commands
            return COMMAND_REGISTRY[command]()