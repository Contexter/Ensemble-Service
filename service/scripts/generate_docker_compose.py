from pathlib import Path
import os
import subprocess

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
SERVICE_ROOT = BASE_DIR
DOCKER_COMPOSE_PATH = SERVICE_ROOT / 'docker-compose.yml'
DOCKERFILE_PATH = SERVICE_ROOT / 'Dockerfile'
REQUIREMENTS_PATH = SERVICE_ROOT / 'requirements.txt'

# Function to verify the repository state
def verify_repository_state():
    """
    Verify if necessary files and directories exist in the repository.
    Ensures SERVICE_ROOT, Dockerfile, requirements.txt, and other dependencies are in place.
    """
    if not SERVICE_ROOT.exists() or not SERVICE_ROOT.is_dir():
        print(f"Error: Service root directory '{SERVICE_ROOT}' does not exist. Please create it before running this script.")
        return False
    if not DOCKERFILE_PATH.exists():
        print(f"Error: Dockerfile '{DOCKERFILE_PATH}' does not exist in the service directory.")
        return False
    if not REQUIREMENTS_PATH.exists():
        print(f"Error: Requirements file '{REQUIREMENTS_PATH}' does not exist in the service directory.")
        return False
    return True

# docker-compose.yml content
docker_compose_content = f"""
version: '3.9'

services:
  fastapi_app:
    build:
      context: ./service
      dockerfile: Dockerfile
    volumes:
      - ./service:/app
    ports:
      - "8000:8000"
    environment:
      - ENV=development
    networks:
      - fountain_network

  typesense:
    image: typesense/typesense:0.24.0
    volumes:
      - typesense_data:/data
    ports:
      - "8108:8108"
    environment:
      - TYPESENSE_API_KEY=${{TYPESENSE_API_KEY}}
    networks:
      - fountain_network

networks:
  fountain_network:
    driver: bridge

volumes:
  typesense_data:
    driver: local
"""

# Function to create the docker-compose.yml file
def create_docker_compose():
    """
    Creates the docker-compose.yml file in the service root directory.
    Ensures that the file does not already exist to maintain idempotency.
    Handles permission errors, file not found errors, and other general exceptions.
    """
    if DOCKER_COMPOSE_PATH.exists():
        print(f"docker-compose.yml already exists at {DOCKER_COMPOSE_PATH}, skipping creation.")
        return
    try:
        # Write the docker-compose.yml file
        with open(DOCKER_COMPOSE_PATH, "w") as docker_compose_file:
            docker_compose_file.write(docker_compose_content.strip())
        print(f"docker-compose.yml created at {DOCKER_COMPOSE_PATH}")
    except PermissionError:
        print(f"Permission denied: unable to create docker-compose.yml at {DOCKER_COMPOSE_PATH}")
    except FileNotFoundError:
        print(f"File not found: unable to create docker-compose.yml at {DOCKER_COMPOSE_PATH}")
    except OSError as e:
        print(f"OS error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

# Main execution
if __name__ == "__main__":
    if verify_repository_state():
        create_docker_compose()
