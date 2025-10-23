# src/security/api_key.py
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

from src.core.settings import app_settings

API_KEY = app_settings.API_TOKEN
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED",
        )
    return api_key
