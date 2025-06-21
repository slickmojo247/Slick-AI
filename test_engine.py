import logging
from engine import SlickLogicEngine
from memory import MemoryBank  # Assuming memory.py exists

def test_engine():
    logging.basicConfig(level=logging.INFO)
    
    # Initialize with mock memory
    memory = MemoryBank(":memory:")
    engine = SlickLogicEngine(memory)
    
    # Test modes
    for mode in ["balanced", "technical", "creative", "homer"]:
        print(f"\nTesting {mode} mode:")
        engine.set_personality_mode(mode)
        response = engine.process_query("Explain quantum computing")
        print(f"Response: {response['response']['content']}")

if __name__ == "__main__":
    test_engine()
