import os
import yaml
from pathlib import Path
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, create_engine, exc, UniqueConstraint, Index, JSON, text
from sqlalchemy.orm import declarative_base, sessionmaker
import logging
import shutil
from dotenv import load_dotenv
import re
from datetime import datetime
from typing import Any
import importlib.util
import sys

# Add the `/service` directory to the system path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define SQLAlchemy Base
Base = declarative_base()

# Regex pattern to validate Python class names
VALID_CLASS_NAME_PATTERN = r'^[A-Za-z_][A-Za-z0-9_]*$'

# Database URL from environment variable
database_url = os.getenv("DATABASE_URL", "sqlite:///service.db")
try:
    engine = create_engine(database_url)
except exc.SQLAlchemyError as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

try:
    engine.connect()
    logger.info("Successfully connected to the database.")
except exc.SQLAlchemyError as e:
    logger.error(f"Database connection failed: {e}")
    raise

# Create a sessionmaker
Session = sessionmaker(bind=engine)

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
        with open(openapi_path, 'r', encoding='utf-8') as file:
            openapi_spec = yaml.safe_load(file)
        if not isinstance(openapi_spec, dict):
            raise ValueError("The OpenAPI specification must be a dictionary.")
        if 'components' not in openapi_spec:
            raise ValueError("The OpenAPI specification is missing the 'components' key.")
        if 'schemas' not in openapi_spec['components']:
            raise ValueError("The OpenAPI specification is missing the 'schemas' key in 'components'.")
        # Validate that 'schemas' is a dictionary
        if not isinstance(openapi_spec['components']['schemas'], dict):
            raise ValueError("The 'schemas' component must be a dictionary.")
        # Additional validation to ensure required sections are present
        for schema_name, schema_details in openapi_spec['components']['schemas'].items():
            if 'properties' not in schema_details:
                raise ValueError(f"The schema '{schema_name}' is missing the 'properties' key.")
        return openapi_spec
    except FileNotFoundError:
        logger.error(f"The OpenAPI specification file at {openapi_path} was not found. Please ensure the file exists at the specified path.")
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
    except Exception as e:
        logger.error(f"An unexpected error occurred while parsing the OpenAPI specification: {e}")
        raise

def get_sqlalchemy_column_type(openapi_type: str) -> Any:
    """
    Map OpenAPI data types to SQLAlchemy column types.
    
    Args:
        openapi_type (str): The OpenAPI type.
    
    Returns:
        SQLAlchemy column type.
    """
    type_mapping = {
        'integer': Integer,
        'string': String,
        'number': Float,
        'boolean': Boolean,
        'object': JSON,
        'array': JSON,
        'date': Date,
        'datetime': DateTime
    }
    return type_mapping.get(openapi_type, String)  # Default to String if type is not supported

def generate_sqlalchemy_models(openapi_spec: dict, models_path: Path) -> None:
    """
    Generate SQLAlchemy models based on the OpenAPI schemas.
    
    Args:
        openapi_spec (dict): Parsed OpenAPI specification.
        models_path (Path): Path where the models will be written.
    
    Returns:
        None
    """
    schemas = openapi_spec.get('components', {}).get('schemas', {})
    if not schemas:
        logger.warning("No schemas found in the OpenAPI specification.")
        return

    for schema_name, schema_details in schemas.items():
        # Validate schema name to ensure it is a valid Python class name
        if not re.match(VALID_CLASS_NAME_PATTERN, schema_name):
            logger.warning(f"Schema name '{schema_name}' is not a valid Python class name. Skipping model generation.")
            continue

        if 'properties' not in schema_details:
            logger.warning(f"Schema '{schema_name}' does not contain 'properties' key. Skipping model generation.")
            continue

        model_code = [
            "from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, UniqueConstraint, Index, JSON",
            "from sqlalchemy.orm import declarative_base",
            "",
            "from app.models.base import Base",
            "",
            f"class {schema_name}(Base):",
            f"    __tablename__ = '{schema_name.lower()}'",
        ]

        properties = schema_details.get('properties', {})
        table_args = []
        primary_key_added = False

        for prop_name, prop_details in properties.items():
            prop_type = prop_details.get('type', 'string')
            column_type = get_sqlalchemy_column_type(prop_type)
            nullable = prop_details.get('nullable', True)
            default = prop_details.get('default', None)
            unique = prop_details.get('unique', False)
            primary_key = prop_details.get('primary_key', False)
            index = prop_details.get('index', False)
            column_definition = f"    {prop_name} = Column({column_type.__name__}, nullable={nullable}"
            if default is not None:
                column_definition += f", default={repr(default)}"
            if unique:
                column_definition += ", unique=True"
            if primary_key:
                column_definition += ", primary_key=True"
                primary_key_added = True
            column_definition += ")"
            model_code.append(column_definition)

            # Collect index if specified
            if index:
                table_args.append(f"Index('{prop_name}_idx', '{prop_name}')")

        # Ensure there is at least one primary key
        if not primary_key_added:
            model_code.append("    id = Column(Integer, primary_key=True, autoincrement=True)")

        if table_args:
            model_code.append(f"    __table_args__ = ({', '.join(table_args)},)" )

        # Write model to file
        model_file_path = models_path / f"{schema_name.lower()}.py"
        if model_file_path.exists():
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            backup_path = model_file_path.with_suffix(f".{timestamp}.bak")
            shutil.copy(model_file_path, backup_path)
            logger.info(f"Backup of the existing model file created at {backup_path}")

        try:
            models_path.mkdir(parents=True, exist_ok=True)
            with model_file_path.open('w', encoding='utf-8') as model_file:
                model_file.write('\n'.join(model_code))
            logger.info(f"{model_file_path} has been created/updated successfully.")
        except PermissionError:
            logger.error(f"Permission denied when attempting to write to {model_file_path}. Please check file permissions.")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while writing to {model_file_path}: {e}")
            raise

def import_models_from_directory(models_path: Path) -> None:
    """
    Import all model files from the specified directory to ensure SQLAlchemy is aware of them.
    
    Args:
        models_path (Path): Path to the directory containing model files.
    
    Returns:
        None
    """
    for model_file in models_path.glob("*.py"):
        if model_file.stem == "__init__":
            continue
        module_name = f"app.models.{model_file.stem}"
        spec = importlib.util.spec_from_file_location(module_name, model_file)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            logger.info(f"Imported model module: {module_name}")

if __name__ == "__main__":
    openapi_path = Path("/service/openapi3_1.yml")
    models_path = Path("/service/app/models")

    try:
        openapi_spec = parse_openapi_spec(openapi_path)
        generate_sqlalchemy_models(openapi_spec, models_path)
        import_models_from_directory(models_path)
        # Create tables in the database
        try:
            Base.metadata.create_all(engine)
            logger.info("Database tables have been created successfully.")
            # Check if tables exist
            with engine.connect() as connection:
                tables = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
                if tables:
                    for table in tables:
                        logger.info(f"Table found: {table[0]}")
                else:
                    logger.warning("No tables were found in the database.")
        except exc.SQLAlchemyError as e:
            logger.error(f"Error occurred during table creation: {e}")
            raise
    except Exception as e:
        logger.error(f"An error occurred during the generation process: {e}")
