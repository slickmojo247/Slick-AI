#!/usr/bin/env python3
"""
Slick Automated Test Runner

Runs:
1. Project structure validation
2. Unit tests
3. Integration tests
4. Service tests
5. Security audit
"""

import os
import sys
import subprocess
import json
import hashlib
# run_tests.py (add error handling)
import traceback

def main():
    try:
        # ... existing test code ...
    except Exception as e:
        print(f"Tests failed due to: {str(e)}")
        traceback.print_exc()
        print("Rolling back to last stable version")
        # Add automatic rollback logic here if needed

if __name__ == "__main__":
    main()
    
TEST_CONFIG = {
    "unit_tests": "pytest tests/unit --color=yes",
    "integration_tests": "pytest tests/integration --color=yes",
    "structure_check": "python tests/cohesion/check_project_structure.py",
    "service_tests": "python tests/manual/test_service_control.py",
    "security_audit": "bandit -r slick"
}

def run_test(name, command):
    """Run a test suite and return results"""
    print(f"\n🚀 Running {name}...")
    print(f"Command: {command}")
    
    result = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    return {
        "name": name,
        "command": command,
        "passed": result.returncode == 0,
        "output": result.stdout,
        "returncode": result.returncode
    }

def generate_report(results):
    """Generate test report"""
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "system": platform.platform(),
        "python_version": platform.python_version(),
        "results": results,
        "summary": {
            "total": len(results),
            "passed": sum(1 for r in results if r["passed"]),
            "failed": sum(1 for r in results if not r["passed"])
        }
    }
    
    # Save report
    os.makedirs("tests/reports", exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    report_file = f"tests/reports/test_report_{timestamp}.json"
    
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    
    return report_file

def main():
    print("🔍 Starting Slick Test Suite")
    print(f"System: {platform.platform()}")
    print(f"Python: {platform.python_version()}\n")
    
    # Run all tests
    results = []
    for name, command in TEST_CONFIG.items():
        results.append(run_test(name, command))
    
    # Generate report
    report_file = generate_report(results)
    
    # Print summary
    print("\n📊 Test Summary:")
    for test in results:
        status = "✅ PASS" if test["passed"] else "❌ FAIL"
        print(f"  {status}: {test['name']}")
    
    print(f"\n📝 Full report saved to: {report_file}")
    
    # Exit with appropriate code
    if all(test["passed"] for test in results):
        print("\n🎉 All tests passed successfully!")
        sys.exit(0)
    else:
        print("\n🔥 Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    import platform
    import time
    main()