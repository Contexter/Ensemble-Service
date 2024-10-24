import os
import logging
from pathlib import Path

# Configure logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# List of directories to be created for the FountainAI Ensemble Service
BASE_DIRS = [
    "app/",
    "app/api/routes/",
    "app/models/",
    "app/schemas/",
    "app/crud/",
    "app/core/",
    "app/auth/",
    "app/typesense/",
    "app/tests/"
]

def create_directory(directory_path):
    """
    Create a directory if it doesn't already exist.

    Args:
        directory_path (str): Path of the directory to be created.
    """
    try:
        # Attempt to create the directory
        os.makedirs(directory_path, exist_ok=True)
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

def main():
    """
    Main function to create all necessary directories.
    Iterates over the list of directories and creates each one.
    """
    for directory in BASE_DIRS:
        create_directory(directory)

if __name__ == "__main__":
    # Execute the main function if the script is run directly
    main()

