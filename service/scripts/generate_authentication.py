import os
import yaml
from pathlib import Path
from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import logging
import re
import shutil
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_openapi_spec(openapi_path: Path) -> dict:
    """
    Parse the OpenAPI specification YAML file.
    
    Args:
        openapi_path (Path): Path to the OpenAPI YAML file.
    
    Returns:
        dict: Parsed OpenAPI specification.
    
    Raises:
        FileNotFoundError: If the OpenAPI file is not found.
        yaml.YAMLError: If there is an error parsing the YAML.
        ValueError: If the OpenAPI spec does not match the expected format.
    """
    try:
        with open(openapi_path, 'r') as file:
            openapi_spec = yaml.safe_load(file)
        if not isinstance(openapi_spec, dict) or 'components' not in openapi_spec or 'securitySchemes' not in openapi_spec['components']:
            raise ValueError("The OpenAPI specification does not have the expected format, or missing required components.")
        # Validate that 'securitySchemes' is a dictionary
        if not isinstance(openapi_spec['components']['securitySchemes'], dict):
            raise ValueError("The 'securitySchemes' component must be a dictionary.")
        return openapi_spec
    except FileNotFoundError:
        logger.error(f"The OpenAPI specification file at {openapi_path} was not found. Please ensure the file exists at the specified path and try again.")
        raise
    except PermissionError:
        logger.error(f"Permission denied when attempting to open {openapi_path}. Please check file permissions.")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing the OpenAPI specification file: {e}")
        raise
    except ValueError as e:
        logger.error(f"Invalid OpenAPI specification format: {e}")
        raise

def generate_authentication_dependencies(openapi_spec: dict, output_path: Path) -> None:
    """
    Generate authentication dependencies based on the OpenAPI security schemes.
    
    Args:
        openapi_spec (dict): Parsed OpenAPI specification.
        output_path (Path): Path where the dependencies file will be written.
    
    Returns:
        None
    """
    # Define security schemes from OpenAPI spec
    security_schemes = openapi_spec.get('components', {}).get('securitySchemes', {})
    if not security_schemes:
        logger.warning("No security schemes found in the OpenAPI specification.")
        return

    # Validate security schemes to ensure they contain expected keys
    for scheme_name, scheme_details in security_schemes.items():
        if not isinstance(scheme_details, dict):
            logger.error(f"Security scheme '{scheme_name}' is not a valid dictionary. Skipping.")
            continue
        if 'type' not in scheme_details or 'in' not in scheme_details:
            logger.error(f"Security scheme '{scheme_name}' is missing required keys ('type' or 'in'). Skipping.")
            continue

    dependencies_code = [
        "from fastapi import Depends, HTTPException, Security",
        "from fastapi.security.api_key import APIKeyHeader",
        "import logging",
        "import os",
        "",
        "logger = logging.getLogger(__name__)",
        "",
    ]

    for scheme_name, scheme_details in security_schemes.items():
        if scheme_details.get('type') == 'apiKey' and scheme_details.get('in') == 'header':
            header_name = scheme_details.get('name', scheme_name)
            # Sanitize header_name to ensure it does not contain invalid characters
            header_name = re.sub(r'[^a-zA-Z0-9-_]', '_', header_name)
            variable_name = f"{scheme_name.lower()}_header"
            dependencies_code.append(f"{variable_name} = APIKeyHeader(name=os.getenv('{scheme_name.upper()}_HEADER_NAME', \"{header_name}\"), auto_error=False)")

            dependencies_code.append(f"def get_{scheme_name.lower()}({variable_name}: str = Security({variable_name})):")
            dependencies_code.append(f"    if not {variable_name} or {variable_name} != os.getenv('{scheme_name.upper()}_VALUE', \"your_{scheme_name.lower()}_key_here\"):")
            dependencies_code.append(f"        logger.error(\"Invalid or missing {scheme_name} provided.\")")
            dependencies_code.append(f"        raise HTTPException(status_code=401, detail=\"Invalid {scheme_name}\")")
            dependencies_code.append(f"    return {variable_name}")
            dependencies_code.append("")

    # Backup the existing output file if it exists
    if output_path.exists():
        backup_path = output_path.with_suffix(output_path.suffix + '.bak')
        try:
            shutil.copy(output_path, backup_path)
            logger.info(f"Backup of the existing output file created at {backup_path}")
        except PermissionError:
            logger.error(f"Permission denied when attempting to create a backup of {output_path}. Please check file permissions.")
            raise

    # Write the generated code to the output file
    try:
        with open(output_path, 'w') as file:
            file.write('\n'.join(dependencies_code))
        logger.info(f"{output_path} has been created/updated successfully.")
    except PermissionError:
        logger.error(f"Permission denied when attempting to write to {output_path}. Please check file permissions.")
        raise

def create_default_env_file(env_path: Path, security_schemes: dict):
    """
    Create a default .env file if it doesn't exist.
    
    Args:
        env_path (Path): Path to the .env file.
        security_schemes (dict): Security schemes from the OpenAPI specification.
    
    Returns:
        None
    """
    if not env_path.exists():
        try:
            with open(env_path, 'w') as env_file:
                env_file.write("# Default environment variables\n")
                for scheme_name, scheme_details in security_schemes.items():
                    if scheme_details.get('type') == 'apiKey' and scheme_details.get('in') == 'header':
                        header_env_name = f"{scheme_name.upper()}_HEADER_NAME"
                        value_env_name = f"{scheme_name.upper()}_VALUE"
                        env_file.write(f"{header_env_name}={scheme_details.get('name', scheme_name)}\n")
                        env_file.write(f"{value_env_name}=your_{scheme_name.lower()}_key_here\n")
            logger.info(f"Default .env file created at {env_path}")
        except PermissionError:
            logger.error(f"Permission denied when attempting to create {env_path}. Please check file permissions.")
            raise

def main() -> None:
    """
    Main function to generate authentication dependencies.
    
    Returns:
        None
    """
    # Define paths
    openapi_path = Path('/service/openapi3_1.yml')
    output_path = Path('/service/app/auth/dependencies.py')
    env_path = Path('/service/.env')

    # Parse the OpenAPI specification
    openapi_spec = parse_openapi_spec(openapi_path)

    # Create a default .env file if it doesn't exist
    security_schemes = openapi_spec.get('components', {}).get('securitySchemes', {})
    create_default_env_file(env_path, security_schemes)

    # Load environment variables from .env file
    load_dotenv(dotenv_path=env_path)

    # Generate the authentication dependencies
    generate_authentication_dependencies(openapi_spec, output_path)

if __name__ == "__main__":
    main()

