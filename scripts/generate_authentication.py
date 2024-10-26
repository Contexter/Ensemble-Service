import os
import yaml
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

# Determine the correct paths based on container mode
container_mode = os.getenv("DOCKER_CONTAINER", "false").lower() == "true"

# Paths adjusted to ensure proper placement in the existing 'auth' folder
auth_path = Path('/service/app/auth') if container_mode else Path('./app/auth')
dependencies_path = auth_path / 'dependencies.py'
openapi_spec_path = Path('/service/openapi3_1.yml') if container_mode else Path('../openapi3_1.yml')

# Ensure the correct OpenAPI spec file path is used
def find_openapi_spec():
    possible_paths = [
        Path('/service/openapi3_1.yml'),
        Path('/service/app/openapi3_1.yml'),
        Path('../openapi3_1.yml')
    ]
    for path in possible_paths:
        if path.exists():
            return path
    raise FileNotFoundError("The OpenAPI specification file could not be found in any of the expected locations.")

def main():
    openapi_spec_path = find_openapi_spec()
    
    try:
        with open(openapi_spec_path, 'r') as file:
            openapi_spec = yaml.safe_load(file)
    except PermissionError:
        raise PermissionError(f"Permission denied when trying to read '{openapi_spec_path}'.")
    except Exception as e:
        raise Exception(f"An error occurred while reading '{openapi_spec_path}': {e}")
    
    api_key_auth = openapi_spec.get('components', {}).get('securitySchemes', {}).get('apiKeyAuth')
    admin_api_key_auth = openapi_spec.get('components', {}).get('securitySchemes', {}).get('adminApiKeyAuth')

    if not api_key_auth:
        raise ValueError("The 'apiKeyAuth' security scheme must be defined in the OpenAPI specification.")
    if not admin_api_key_auth:
        raise ValueError("The 'adminApiKeyAuth' security scheme must be defined in the OpenAPI specification.")

    dependencies_content = """
from fastapi import HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
import os

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
admin_api_key_header = APIKeyHeader(name="X-Admin-API-Key", auto_error=False)

API_KEYS = os.getenv("API_KEYS", "your_standard_api_key").split(",")  # Load from environment variable
ADMIN_API_KEYS = os.getenv("ADMIN_API_KEYS", "your_admin_api_key").split(",")  # Load from environment variable

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key not in API_KEYS:
        raise HTTPException(status_code=403, detail="Could not validate API Key")
    return api_key

def get_admin_api_key(admin_api_key: str = Security(admin_api_key_header)):
    if admin_api_key not in ADMIN_API_KEYS:
        raise HTTPException(status_code=403, detail="Could not validate Admin API Key")
    return admin_api_key
    """

    # Ensure the directory exists
    try:
        dependencies_path.parent.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        raise PermissionError(f"Permission denied when trying to create directory '{dependencies_path.parent}'.")
    except Exception as e:
        raise Exception(f"An error occurred while creating directory '{dependencies_path.parent}': {e}")
    
    # Write the content to the dependencies.py file
    with open(dependencies_path, 'w') as file:
        file.write(dependencies_content)

    logging.info(f"'{dependencies_path}' has been created/updated successfully.")

if __name__ == "__main__":
    main()
