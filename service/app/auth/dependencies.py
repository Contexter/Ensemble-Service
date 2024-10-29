from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import logging
import os

logger = logging.getLogger(__name__)

apikeyauth_header = APIKeyHeader(name=os.getenv('APIKEYAUTH_HEADER_NAME', "X-API-KEY"), auto_error=False)
def get_apikeyauth(apikeyauth_header: str = Security(apikeyauth_header)):
    if not apikeyauth_header or apikeyauth_header != os.getenv('APIKEYAUTH_VALUE', "your_apikeyauth_key_here"):
        logger.error("Invalid or missing apiKeyAuth provided.")
        raise HTTPException(status_code=401, detail="Invalid apiKeyAuth")
    return apikeyauth_header

adminapikeyauth_header = APIKeyHeader(name=os.getenv('ADMINAPIKEYAUTH_HEADER_NAME', "X-ADMIN-API-KEY"), auto_error=False)
def get_adminapikeyauth(adminapikeyauth_header: str = Security(adminapikeyauth_header)):
    if not adminapikeyauth_header or adminapikeyauth_header != os.getenv('ADMINAPIKEYAUTH_VALUE', "your_adminapikeyauth_key_here"):
        logger.error("Invalid or missing adminApiKeyAuth provided.")
        raise HTTPException(status_code=401, detail="Invalid adminApiKeyAuth")
    return adminapikeyauth_header
