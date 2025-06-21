# tests/start_test_services.py
import subprocess
import time
import threading
from slick.core.service_manager import ServiceManager

def start_test_environment():
    # Start core services
    services = [
        {"name": "slick-controller", "command": "uvicorn slick.api.main:app --port 8000"},
        {"name": "redis", "command": "redis-server"},
        {"name": "test-web", "command": "python -m http.server 8080"}
    ]
    
    manager = ServiceManager()
    for service in services:
        manager.add_service(service)
        manager.start_service(service["name"])
    
    # Start mock AI endpoints
    ai_services = {
        "mock-openai": "python tests/mocks/mock_openai.py",
        "mock-deepseek": "python tests/mocks/mock_deepseek.py"
    }
    
    for name, cmd in ai_services.items():
        manager.add_service({"name": name, "command": cmd})
        manager.start_service(name)
    
    print("Test services started:")
    for service in manager.get_all_services():
        print(f"- {service['name']} ({service['status']})")
    
    # Keep running until interrupted
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping test services...")
        for service in manager.get_all_services():
            manager.stop_service(service["id"])

if __name__ == "__main__":
    start_test_environment()