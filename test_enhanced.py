from ai_core import APIOrchestrator
from ai_core.middleware.usage_tracker import UsageTracker

@UsageTracker()
def test_enhanced():
    print("Testing Enhanced AI Core...")
    
    orchestrator = APIOrchestrator()
    
    # Test technical query
    tech_response = orchestrator.route_query(
        "Explain Python decorators",
        context={"mode": "technical"}
    )
    print("Technical Response:", tech_response["response"]["content"])
    
    # Test creative query
    creative_response = orchestrator.route_query(
        "Write a poem about AI",
        context={"mode": "creative"}
    )
    print("Creative Response:", creative_response["response"]["content"])

if __name__ == "__main__":
    test_enhanced()
