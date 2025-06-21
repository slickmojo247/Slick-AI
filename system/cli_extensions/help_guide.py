def show_developer_guide():
    print("\nSLICK AI DEVELOPER MANUAL")
    print("="*60)
    print("Core Architecture Principles:")
    print("- Modular command system")
    print("- CSV-driven configuration")
    print("- ThinkSession-based learning")
    print("- Self-healing file structure")
    
    print("\nAdvanced Function Linking Guide:")
    print("1. Creating New Commands:")
    print("   a. Create file in slick/commands/")
    print("   b. Template:")
    print('''\
from core.CommandInterface import CommandBase

class NewCommand(CommandBase):
    def execute(self, args):
        \"\"\"Implementation here\"\"\"
        return "Result"
    ''')
    print("   c. Register in command_registry.csv")
    
    print("\n2. Extending AI Capabilities:")
    print("   - Logic chains: query 'Then scan engine'")
    print("   - Auto-implement in SlickLogicEngine:")
    print('''\
def process_chain(self, query):
    if "then" in query:
        commands = query.split("then")
        for cmd in commands:
            self.cli.onecmd(cmd.strip())
    ''')
    
    print("\n3. Custom CSV Processors:")
    print("   - Create processor in system/cli_extensions/csv_handlers/")
    print("   - Implement handle_<filename_pattern>.py")
    print("   - Example: handle_project_report.py")
    
    print("\n4. GitHub Integration:")
    print("   !git <command> - Direct shell access")
    print("   sync before commit - Ensures clean state")
    print("   rescan_and_verify.py - Pre-commit hook")
    
    print("\n5. ThinkSession Processing Pipeline:")
    print("   Raw entry -> think_sessions_processor.py ->")
    print("   memory/MemoryBank.py -> personality_profile.json")
    
    print("\n6. Debugging Tools:")
    print("   log debug - Enable verbose logging")
    print("   status - System health check")
    print("   validate - Consistency verification")
