# tests/post_reset_validation.py
def validate_system():
    checks = [
        verify_core_modules(),
        check_database_consistency(),
        test_knowledge_graph_links(),
        validate_memory_decay_rates()
    ]
    return all(checks)

def verify_core_modules():
    required_modules = ['logic_core', 'memory_system', 'knowledge_engine']
    return all(importlib.util.find_spec(m) for m in required_modules)