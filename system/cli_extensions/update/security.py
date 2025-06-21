# utils/security.py
from fastapi.security import APIKeyHeader
from fastapi import HTTPException, status

class APIKeyHeader(APIKeyHeader):
    async def __call__(self, request):
        api_key = await super().__call__(request)
        if not self._validate_key(api_key):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid API Key"
            )
        return api_key
    
    def _validate_key(self, key: str) -> bool:
        # Implement your key validation logic
        return key == os.getenv('API_SECRET_KEY')