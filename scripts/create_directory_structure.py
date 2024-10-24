import os
import logging
import shutil
from pathlib import Path

# Configure logging settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
LOG_FORMAT = os.getenv('LOG_FORMAT', '%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

# Define the base path to ensure the app directory is created at the correct level
BASE_PATH = Path(__file__).resolve().parent.parent

# List of directories to be created for the FountainAI Ensemble Service
BASE_DIRS = [
    BASE_PATH / "app/",
    BASE_PATH / "app/api/routes/",
    BASE_PATH / "app/models/",
    BASE_PATH / "app/schemas/",
    BASE_PATH / "app/crud/",
    BASE_PATH / "app/core/",
    BASE_PATH / "app/auth/",
    BASE_PATH / "app/typesense/",
    BASE_PATH / "app/tests/",
    BASE_PATH / "app/utils/"
]

ADDITIONAL_FILES = [
    BASE_PATH / "app/main.py",
    BASE_PATH / "app/config.py",
    BASE_PATH / "app/dependencies.py",
    BASE_PATH / "app/api/routes/__init__.py",
    BASE_PATH / "app/models/__init__.py",
    BASE_PATH / "app/schemas/__init__.py",
    BASE_PATH / "app/crud/__init__.py",
    BASE_PATH / "app/core/__init__.py",
    BASE_PATH / "app/auth/__init__.py",
    BASE_PATH / "app/typesense/__init__.py",
    BASE_PATH / "app/tests/__init__.py",
    BASE_PATH / "app/utils/__init__.py"
]

def delete_existing_directories():
    """
    Delete all previously created directories to ensure the script is idempotent.
    """
    confirmation = input("Are you sure you want to delete existing directories? This action cannot be undone. (yes/no): ")
    if confirmation.lower() != 'yes':
        logging.info("Deletion of existing directories was canceled.")
        return

    for directory in reversed(BASE_DIRS):
        try:
            if directory.exists():
                shutil.rmtree(directory)
                logging.info(f"Directory '{directory}' deleted successfully.")
        except OSError as e:
            logging.error(f"OSError: Error deleting directory '{directory}': {e}")

def create_directory(directory_path):
    """
    Create a directory if it doesn't already exist.

    Args:
        directory_path (Path): Path of the directory to be created.
    """
    try:
        # Attempt to create the directory
        directory_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Directory '{directory_path}' created successfully.")
    except FileNotFoundError as e:
        # Handle error if the directory path is invalid
        logging.error(f"FileNotFoundError: Error creating directory '{directory_path}': {e}")
    except PermissionError as e:
        # Handle error if there are insufficient permissions
        logging.error(f"PermissionError: Error creating directory '{directory_path}': {e}")
    except OSError as e:
        # Handle other OS-related errors
        logging.error(f"OSError: Error creating directory '{directory_path}': {e}")

def create_file(file_path):
    """
    Create an empty file if it doesn't already exist.

    Args:
        file_path (Path): Path of the file to be created.
    """
    try:
        if not file_path.exists():
            file_path.touch()
            logging.info(f"File '{file_path}' created successfully.")
        else:
            logging.info(f"File '{file_path}' already exists. Skipping creation.")
    except OSError as e:
        logging.error(f"OSError: Error creating file '{file_path}': {e}")

def main():
    """
    Main function to delete existing directories and create all necessary directories and files.
    Iterates over the list of directories and files and creates each one.
    """
    # Delete existing directories
    delete_existing_directories()

    # Create directories
    for directory in BASE_DIRS:
        create_directory(directory)

    # Create necessary files
    for file in ADDITIONAL_FILES:
        create_file(file)

if __name__ == "__main__":
    # Execute the main function if the script is run directly
    main()
