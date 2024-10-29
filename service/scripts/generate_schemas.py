import os
import yaml
from pathlib import Path
from pydantic import BaseModel, Field, constr, conint
import inflect
from inflect import engine
import logging
import re
from typing import Any, List, Literal

# Initialize inflect engine for pluralization and singularization
inflect_engine = inflect.engine()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_openapi_spec(openapi_path):
    try:
        with open(openapi_path, 'r') as file:
            openapi_spec = yaml.safe_load(file)
        if not isinstance(openapi_spec, dict) or 'components' not in openapi_spec:
            raise ValueError("The OpenAPI specification does not have the expected format.")
        return openapi_spec
    except FileNotFoundError:
        logger.error(f"The OpenAPI specification file at {openapi_path} was not found. Please ensure the file exists at the specified path and try again.")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing the OpenAPI specification file: {e}")
        raise
    except ValueError as e:
        logger.error(f"Invalid OpenAPI specification format: {e}")
        raise

def sanitize_schema_name(schema_name):
    # Sanitize schema_name to ensure it is a valid Python class name
    schema_name = re.sub(r'[^a-zA-Z0-9_]', '', schema_name)
    if schema_name[0].isdigit():
        schema_name = f'_{schema_name}'
    return schema_name

def sanitize_enum_values(enum_values):
    # Sanitize enum values to ensure they are valid Python identifiers
    return [re.sub(r'[^a-zA-Z0-9_]', '_', str(value)) for value in enum_values]

def generate_pydantic_model(schema_name, schema_properties):
    sanitized_name = sanitize_schema_name(schema_name)
    class_definition = [f'class {sanitized_name}(BaseModel):']
    
    for prop, details in schema_properties.items():
        prop_type = details.get('type', 'str')
        constraints = []

        # Handle different property types
        if prop_type == 'string':
            prop_type = 'str'
            if 'maxLength' in details:
                constraints.append(f"max_length={details['maxLength']}")
            if 'minLength' in details:
                constraints.append(f"min_length={details['minLength']}")
            if 'pattern' in details:
                constraints.append(f"regex=r'{details['pattern']}'")
        elif prop_type == 'integer':
            prop_type = 'int'
            if 'minimum' in details:
                constraints.append(f"ge={details['minimum']}")
            if 'maximum' in details:
                constraints.append(f"le={details['maximum']}")
        elif prop_type == 'boolean':
            prop_type = 'bool'
        elif prop_type == 'array':
            items = details.get('items', {})
            if items.get('type') == 'object':
                nested_schema_name = sanitize_schema_name(f"{schema_name}_{prop}_item")
                nested_properties = items.get('properties', {})
                nested_model_code = generate_pydantic_model(nested_schema_name, nested_properties)
                write_model_to_file(nested_schema_name, nested_model_code, Path('/service/app/schemas/'))
                prop_type = f'List[{nested_schema_name}]'
            else:
                item_type = items.get('type', 'Any')
                prop_type = f'List[{item_type}]'
        elif prop_type == 'object':
            prop_type = 'dict'
        elif 'enum' in details:
            enum_values = sanitize_enum_values(details['enum'])
            prop_type = f'Literal{tuple(enum_values)}'
        
        # Generate field code with constraints
        if constraints:
            field_constraints = ', '.join(constraints)
            field_code = f'Field(..., {field_constraints})'
        else:
            field_code = 'Field(...)'
        
        class_definition.append(f'    {prop}: {prop_type} = {field_code}')
    
    class_definition.append('')  # Blank line at the end of the class
    return '\n'.join(class_definition)

def write_model_to_file(schema_name, model_code, schemas_dir):
    file_path = schemas_dir / f"{re.sub(r'(?<!^)(?=[A-Z])', '_', schema_name).lower()}.py"
    with open(file_path, 'w') as file:
        file.write(model_code)
    logger.info(f"{file_path} has been created/updated successfully.")

def generate_schemas():
    # Define paths
    openapi_path = Path('/service/openapi3_1.yml')
    schemas_dir = Path('/service/app/schemas/')

    # Ensure the schemas directory exists
    try:
        schemas_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Schemas directory at {schemas_dir} created successfully.")
    except Exception as e:
        logger.error(f"Error creating schemas directory: {e}")
        raise

    # Parse the OpenAPI specification
    openapi_spec = parse_openapi_spec(openapi_path)
    schemas = openapi_spec.get('components', {}).get('schemas', {})

    # Generate Pydantic models
    for schema_name, schema_details in schemas.items():
        properties = schema_details.get('properties', {})
        model_code = generate_pydantic_model(schema_name, properties)
        write_model_to_file(schema_name, model_code, schemas_dir)

if __name__ == "__main__":
    generate_schemas()
