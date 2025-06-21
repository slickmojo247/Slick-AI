# verify.py
def verify():
    required = [
        'core/application.py',
        'services/ai/connector.py',
        'interfaces/web/dashboard.html'
    ]
    
    missing = [f for f in required if not os.path.exists(f)]
    if missing:
        print(f"Missing files: {missing}")
        return False
        
    print("System verified successfully!")
    return True
