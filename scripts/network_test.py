import socket
import requests
from pathlib import Path

def test_connection():
    tests = {
        "DNS Resolution": lambda: socket.gethostbyname('api.deepseek.ai'),
        "HTTPS Connection": lambda: requests.get('https://api.deepseek.ai', timeout=5).status_code,
        "API Endpoint": lambda: requests.get('https://api.deepseek.ai/v1', timeout=5).status_code
    }
    
    results = {}
    for name, test in tests.items():
        try:
            result = test()
            results[name] = ("✓ Success", result)
        except Exception as e:
            results[name] = ("✗ Failed", str(e))
    
    print("\nNetwork Diagnostics:")
    for name, (status, detail) in results.items():
        print(f"{name:<20} {status:<15} {detail}")

if __name__ == "__main__":
    test_connection()
