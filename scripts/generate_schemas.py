import yaml
import os
from pathlib import Path
from pydantic import BaseModel
import logging

# Configure logging settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
LOG_FORMAT = os.getenv('LOG_FORMAT', '%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

# Define the base path to ensure the schemas are generated in the correct place
BASE_PATH = Path(__file__).resolve().parent.parent
OPENAPI_FILE = BASE_PATH / "openapi3_1.yml"
SCHEMAS_OUTPUT_FILE = BASE_PATH / "app/schemas/models.py"

def load_openapi_spec():
    """
    Load the OpenAPI specification from the YAML file.

    Returns:
        dict: Parsed OpenAPI specification.
    """
    if not OPENAPI_FILE.exists():
        logging.error(f"OpenAPI file not found: {OPENAPI_FILE}")
        return None
    
    try:
        with open(OPENAPI_FILE, 'r') as file:
            openapi_spec = yaml.safe_load(file)
            logging.info("OpenAPI specification loaded successfully.")
            return openapi_spec
    except yaml.YAMLError as e:
        logging.error(f"Error parsing OpenAPI file: {e}")
        return None

def generate_pydantic_models(openapi_spec):
    """
    Generate Pydantic models from the OpenAPI specification.

    Args:
        openapi_spec (dict): The OpenAPI specification.
    """
    if not openapi_spec:
        raise ValueError("No OpenAPI specification available to generate models.")

    components = openapi_spec.get("components", {})
    schemas = components.get("schemas", {})

    if not schemas:
        logging.error("No schemas found in the OpenAPI specification.")
        return

    try:
        # Only open the file if schemas exist
        with open(SCHEMAS_OUTPUT_FILE, 'w') as file:
            file.write("from pydantic import BaseModel\n\n")

            for schema_name, schema in schemas.items():
                file.write(f"class {schema_name}(BaseModel):\n")
                properties = schema.get("properties", {})
                required_fields = schema.get("required", [])

                for prop_name, prop_attrs in properties.items():
                    prop_type = prop_attrs.get("type", "str")
                    field_type = "str"  # Default type

                    if prop_type == "integer":
                        field_type = "int"
                    elif prop_type == "number":
                        field_type = "float"
                    elif prop_type == "boolean":
                        field_type = "bool"
                    elif prop_type == "array":
                        items = prop_attrs.get('items', {})
                        item_type = items.get('type', 'str')
                        if item_type == "object":
                            field_type = f"list[dict]"
                        elif item_type == "array":
                            field_type = f"list[list[{items.get('items', {}).get('type', 'str')}]]"
                        else:
                            field_type = f"list[{item_type}]"
                    elif prop_type == "object":
                        field_type = "dict"

                    is_required = prop_name in required_fields
                    if is_required:
                        file.write(f"    {prop_name}: {field_type}\n")
                    else:
                        file.write(f"    {prop_name}: {field_type} = None\n")

                file.write("\n")

            logging.info("Pydantic models generated successfully.")
    except OSError as e:
        logging.error(f"OSError: Error writing to schemas file '{SCHEMAS_OUTPUT_FILE}': {e}")

def main():
    """
    Main function to load the OpenAPI specification and generate Pydantic models.
    """
    openapi_spec = load_openapi_spec()
    generate_pydantic_models(openapi_spec)

if __name__ == "__main__":
    # Execute the main function if the script is run directly
    main()

