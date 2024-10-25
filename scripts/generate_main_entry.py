# generate_main_entry.py

import os
import logging
from pathlib import Path

# Path to the main.py file
MAIN_FILE_PATH = Path('app/main.py')

# Path to the input OpenAPI specification
INPUT_OPENAPI_SPEC_PATH = 'openapi3_1.yml'

# Ensure that the app directory exists
APP_DIR_PATH = MAIN_FILE_PATH.parent
if not APP_DIR_PATH.exists():
    APP_DIR_PATH.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Generate main.py content
def generate_main_file():
    parts = [
        "from fastapi import FastAPI\n",
        "import yaml\n\n",
        "app = FastAPI()\n\n",
        "# Load input OpenAPI specification\n",
        f"def load_openapi_spec():\n    with open('{INPUT_OPENAPI_SPEC_PATH}', 'r') as file:\n        return yaml.safe_load(file)\n\n",
        "# Example root endpoint\n",
        "@app.get(\"/\")\n",
        "def read_root():\n    return {\"message\": \"Hello, World!\"}\n\n",
        "# Additional routes can be added here\n"
    ]
    main_content = "".join(parts)
    
    # Write main.py file
    with open(MAIN_FILE_PATH, 'w') as main_file:
        main_file.write(main_content)
    logging.info(f"Generated {MAIN_FILE_PATH}")

if __name__ == "__main__":
    generate_main_file()

