# generate_schemas.py

import yaml
import os
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List, Union, Literal, Type
from pathlib import Path
from enum import Enum

# Path to the OpenAPI specification
OPENAPI_SPEC_PATH = os.getenv('OPENAPI_SPEC_PATH', '/app/openapi3_1.yml')  # Input OpenAPI specification
# Directory to store generated Pydantic models
SCHEMAS_DIR = Path(os.getenv('SCHEMAS_DIR', '/app/app/schemas'))

# Ensure the schemas directory exists
SCHEMAS_DIR.mkdir(parents=True, exist_ok=True)

# Load the OpenAPI specification
try:
    with open(OPENAPI_SPEC_PATH, 'r') as file:
        openapi_spec = yaml.safe_load(file)
except FileNotFoundError:
    raise FileNotFoundError(f"The OpenAPI specification file '{OPENAPI_SPEC_PATH}' was not found.")
except yaml.YAMLError as e:
    raise RuntimeError(f"Failed to load OpenAPI specification: {e}")
except PermissionError:
    raise PermissionError(f"Permission denied when trying to read the OpenAPI specification file '{OPENAPI_SPEC_PATH}'")

# Function to generate Pydantic models from OpenAPI components
class PydanticModelGenerator:
    def __init__(self, components: Dict[str, Any]):
        self.components = components

    def generate_models(self):
        for model_name, model_spec in self.components.get('schemas', {}).items():
            self.generate_model(model_name, model_spec)

    def generate_model(self, model_name: str, model_spec: Dict[str, Any]):
        class_code = [f"class {model_name}(BaseModel):"]
        properties = model_spec.get('properties', {})
        required_fields = model_spec.get('required', [])

        for prop_name, prop_spec in properties.items():
            prop_type = self.get_python_type(prop_spec)
            default = "..." if prop_name in required_fields else "None"
            if prop_spec.get('nullable', False):
                prop_type = f'Optional[{prop_type}]'
            class_code.append(f"    {prop_name}: {prop_type} = Field({default})")

        # Handle case for empty models
        if not properties:
            class_code.append("    pass  # No properties defined for this model")

        # Write model to file
        model_file_path = SCHEMAS_DIR / f"{model_name.lower()}.py"
        if not model_file_path.exists():
            with model_file_path.open('w') as model_file:
                model_file.write('\n'.join(class_code))

    def get_python_type(self, prop_spec: Dict[str, Any]) -> str:
        openapi_type = prop_spec.get('type')
        format_type = prop_spec.get('format')

        if openapi_type == 'string':
            if 'enum' in prop_spec:
                enum_name = f"{prop_spec.get('title', 'Enum')}"
                self.generate_enum(enum_name, prop_spec['enum'])
                return enum_name
            if format_type == 'date':
                return 'date'
            if format_type == 'date-time':
                return 'datetime'
            if format_type == 'uuid':
                return 'UUID'
            return 'str'
        elif openapi_type == 'integer':
            return 'int'
        elif openapi_type == 'boolean':
            return 'bool'
        elif openapi_type == 'number':
            return 'float'
        elif openapi_type == 'array':
            items_type = self.get_python_type(prop_spec.get('items', {}))
            return f'List[{items_type}]'
        elif openapi_type == 'object':
            if 'properties' in prop_spec:
                return f"Dict[str, Any]"
            return 'Dict[str, Any]'
        elif openapi_type == 'null':
            return 'Optional[Any]'
        elif openapi_type == 'binary':
            return 'bytes'
        elif openapi_type == 'enum':
            return 'Enum'
        else:
            return 'Any'

    def generate_enum(self, enum_name: str, enum_values: List[Any]):
        enum_code = [f"class {enum_name}(str, Enum):"]
        for value in enum_values:
            enum_code.append(f"    {value.upper()} = '{value}'")
        # Write enum to file
        enum_file_path = SCHEMAS_DIR / f"{enum_name.lower()}.py"
        if not enum_file_path.exists():
            with enum_file_path.open('w') as enum_file:
                enum_file.write('\n'.join(enum_code))

# Generate Pydantic models
if 'components' in openapi_spec and 'schemas' in openapi_spec['components']:
    generator = PydanticModelGenerator(openapi_spec['components'])
    generator.generate_models()
