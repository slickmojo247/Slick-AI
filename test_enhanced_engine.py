import logging
from engine import SlickLogicEngine
from memory import MemoryBank

def test_enhanced():
    logging.basicConfig(level=logging.INFO)
    memory = MemoryBank(":memory:")
    engine = SlickLogicEngine(memory)
    
    # Test processing with context
    response = engine.process_query(
        "Explain quantum computing to a 5 year old",
        {"user_level": "child"}
    )
    print("Response:", response["response"]["content"])
    
    # Provide feedback
    engine.provide_feedback({
        "query": "Explain quantum computing",
        "comment": "too technical",
        "suggestion": "use simpler analogies"
    })
    
    # Get performance report
    print("Performance:", engine.get_performance_report())

if __name__ == "__main__":
    test_enhanced()
