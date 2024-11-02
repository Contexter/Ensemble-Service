#!/usr/bin/env python3

import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_ROOT = BASE_DIR
DOCKERFILE_PATH = os.path.join(SERVICE_ROOT, 'Dockerfile')
DOCKERIGNORE_PATH = os.path.join(BASE_DIR, '.dockerignore')
REQUIREMENTS_PATH = os.path.join(SERVICE_ROOT, 'requirements.txt')

# Dockerfile content
dockerfile_content = """
# Use an official Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /service

# Install required system packages
RUN apt-get update
RUN apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy application code and scripts into the container
COPY ./service/ /service/
COPY ./service/requirements.txt /service/requirements.txt

# Create and activate a virtual environment
RUN python -m venv /service/venv
ENV PATH="/service/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --no-cache-dir -r /service/requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set CMD to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

# .dockerignore content
dockerignore_content = """
*.pyc
__pycache__
*.pyo
*.pyd
.DS_Store
.git
.gitignore
create_backup_and_prepare_next_iteration.sh
"""

# Requirements.txt content
requirements_content = """
fastapi==0.95.2
uvicorn==0.21.1
alembic==1.10.4
SQLAlchemy==2.0.15
psycopg2-binary==2.9.6
"""

# Function to check the state of the repository
def check_repo_state():
    """
    Checks the state of the repository to ensure necessary files and directories exist before proceeding.
    Prints messages indicating whether each required file or directory is present.
    """
    if not os.path.exists(SERVICE_ROOT):
        print(f"Error: Service root directory '{SERVICE_ROOT}' does not exist. Please create it before running this script.")
        return False
    return True

# Function to create the Dockerfile
def create_dockerfile():
    """
    Creates the Dockerfile in the service root directory if it does not already exist.
    Ensures that the service root directory exists, writes the Dockerfile content, and verifies that the content was written correctly.
    Handles permission errors, file not found errors, and other general exceptions.
    """
    if os.path.exists(DOCKERFILE_PATH):
        print(f"Dockerfile already exists at {DOCKERFILE_PATH}, skipping creation.")
        return
    try:
        # Write the Dockerfile
        with open(DOCKERFILE_PATH, "w") as dockerfile:
            dockerfile.write(dockerfile_content.strip())
        
        # Verify that the content was written correctly
        with open(DOCKERFILE_PATH, "r") as verify_file:
            written_content = verify_file.read().strip()
            if written_content != dockerfile_content.strip():
                print(f"Warning: Discrepancy found in the written Dockerfile at {DOCKERFILE_PATH}")
        print(f"Dockerfile created at {DOCKERFILE_PATH}")
    except PermissionError:
        print(f"Permission denied: unable to create Dockerfile at {DOCKERFILE_PATH}")
    except FileNotFoundError:
        print(f"File not found: unable to create Dockerfile at {DOCKERFILE_PATH}")
    except Exception as e:
        print(f"Error creating Dockerfile: {e}")

# Function to create the .dockerignore file
def create_dockerignore():
    """
    Creates the .dockerignore file in the base directory if it does not already exist.
    Writes the specified .dockerignore content and handles permission errors, file not found errors, and other general exceptions.
    """
    if os.path.exists(DOCKERIGNORE_PATH):
        print(f".dockerignore already exists at {DOCKERIGNORE_PATH}, skipping creation.")
        return
    try:
        with open(DOCKERIGNORE_PATH, "w") as dockerignore:
            dockerignore.write(dockerignore_content.strip())
        print(f".dockerignore created at {DOCKERIGNORE_PATH}")
    except PermissionError:
        print(f"Permission denied: unable to create .dockerignore at {DOCKERIGNORE_PATH}")
    except FileNotFoundError:
        print(f"File not found: unable to create .dockerignore at {DOCKERIGNORE_PATH}")
    except Exception as e:
        print(f"Error creating .dockerignore: {e}")

# Function to create the requirements.txt file
def create_requirements():
    """
    Creates the requirements.txt file in the service root directory if it does not already exist.
    Writes the specified requirements content and handles permission errors, file not found errors, and other general exceptions.
    """
    if os.path.exists(REQUIREMENTS_PATH):
        print(f"requirements.txt already exists at {REQUIREMENTS_PATH}, skipping creation.")
        return
    try:
        with open(REQUIREMENTS_PATH, "w") as requirements_file:
            requirements_file.write(requirements_content.strip())
        print(f"requirements.txt created at {REQUIREMENTS_PATH}")
    except PermissionError:
        print(f"Permission denied: unable to create requirements.txt at {REQUIREMENTS_PATH}")
    except FileNotFoundError:
        print(f"File not found: unable to create requirements.txt at {REQUIREMENTS_PATH}")
    except Exception as e:
        print(f"Error creating requirements.txt: {e}")

# Main execution
if __name__ == "__main__":
    """
    Main execution function to create necessary files for the Docker setup.
    Calls functions to create the Dockerfile, .dockerignore, and requirements.txt files after checking the repository state.
    """
    if check_repo_state():
        create_requirements()
        create_dockerfile()
        create_dockerignore()
