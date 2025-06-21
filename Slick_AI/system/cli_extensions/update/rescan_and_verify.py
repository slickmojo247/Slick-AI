import os
import csv

EXPECTED_STRUCTURE = {
    'main.py': '/',
    'SlickLogicEngine.py': 'engine/',
    'MemoryBank.py': 'memory/',
    'APIOrchestrator.py': 'ai_core/',
    'Slick_AI_Command_Interface.py': 'core/'
}

def verify_structure():
    discrepancies = []
    for file, path in EXPECTED_STRUCTURE.items():
        full_path = os.path.join(path, file)
        if not os.path.exists(full_path):
            discrepancies.append(f"Missing: {full_path}")
    return discrepancies

if __name__ == "__main__":
    issues = verify_structure()
    if issues:
        print("⚠️ Structure issues found:")
        for issue in issues:
            print(issue)
    else:
        print("✅ All files in correct locations")
