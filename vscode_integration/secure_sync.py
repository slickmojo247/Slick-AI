class SecureSync:
    def __init__(self):
        print("⚠️ No cryptography/JWT installed. Running in mock mode.")
    
    def encrypt(self, data: str) -> str:
        return f"mock_encrypted:{data}"
    
    def decrypt(self, token: str) -> str:
        return token.replace("mock_encrypted:", "")
    
    def generate_jwt(self, user_id: str) -> str:
        return f"mock_jwt:{user_id}"
