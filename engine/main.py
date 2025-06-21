#!/usr/bin/env python3
"""
SLICK AI v2.1 - Complete System
"""

import logging
import cmd
from engine.SlickLogicEngine import SlickLogicEngine
from memory.MemoryBank import MemoryBank
from ai_core.APIOrchestrator import APIOrchestrator

class SlickAI(cmd.Cmd):
    prompt = "SLICK> "
    
    def __init__(self):
        super().__init__()
        self._setup_logging()
        self.memory = MemoryBank()
        self.engine = SlickLogicEngine(self.memory)
        self.api = APIOrchestrator()
        self.log.info("System initialized")

    def _setup_logging(self):
        self.log = logging.getLogger("SlickAI")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("slick.log"),
                logging.StreamHandler()
            ]
        )

    def do_query(self, arg):
        """Process a query: QUERY <your question>"""
        try:
            result = self.engine.process(arg)
            api_response = self.api.route(result)
            print(f"\n{api_response}\n")
        except Exception as e:
            self.log.error(f"Query failed: {e}")
            print(f"Error: {e}")

    def do_mode(self, arg):
        """Change personality mode: MODE <balanced|technical|creative|homer>"""
        try:
            self.engine.set_mode(arg)
            print(f"Mode set to {arg}")
        except ValueError as e:
            print(f"Error: {e}")

    def do_exit(self, arg):
        """Exit the system"""
        self.log.info("Shutting down")
        print("Goodbye!")
        return True

if __name__ == "__main__":
    print("SLICK AI SYSTEM - Version 2.1")
    SlickAI().cmdloop()
