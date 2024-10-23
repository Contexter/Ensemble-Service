#!/bin/bash

# Reference: This script is based on the OpenAPI specification for the FountainAI Ensemble Service, which can be found at: https://github.com/Contexter/FountainAI/blob/main/openAPI/v4/Ensemble-Service.yml

# Prompt: This script is designed to create the directory structure, placeholder files, and a Dockerfile for a FastAPI application based on the FountainAI Ensemble Service. Ensure that all necessary components for the application are present, including directories for prompts, interactions, logs, schemas, routes, models, utilities, configurations, services, and repositories. The script must be executed from the root of the https://github.com/Contexter/Ensemble-Service repository to properly set up the environment.

# Use this prompt to test for consistency in a GPT-4 Canvas session. 

set -e

# Directory paths
# Each directory in this list is used to represent a specific component of the FastAPI application.
directories=(
  "./app/prompt_factory"  # Manages system prompts for the Assistant.
  "./app/interactions"    # Manages interaction flow.
  "./app/logs"            # Stores logs for user inputs, responses, and interactions.
  "./app/schemas"         # Stores JSON schemas for request and response validation.
  "./doc"                 # Stores the input OpenAPI specification.
  "./app/main"            # Contains the main application entry point.
  "./app/routers"         # Defines API routes.
  "./app/models"          # Defines data models used by the application.
  "./app/utils"           # Contains utility/helper functions.
  "./app/config"          # Stores configuration files.
  "./app/services"        # Contains business logic and service handlers.
  "./app/repositories"    # Manages data persistence and repository logic.
)

# Create placeholder files to ensure directories are committed
create_placeholder_files() {
  echo "Creating placeholder files..."
  for dir in "${directories[@]}"; do
    touch "$dir/.gitkeep"
    echo "Created placeholder file in: $dir"
  done

  # Create placeholder Python files for FastAPI structure
  touch "./app/main/main.py"
  touch "./app/routers/gui.py"
  touch "./app/routers/kong.py"
  touch "./app/models/schemas.py"
  touch "./app/utils/helpers.py"
  touch "./app/config/config.py"
  touch "./app/services/service_handler.py"
  touch "./app/repositories/repository.py"

  echo "Created placeholder Python files for FastAPI structure."

  # Create Dockerfile for deployment
  echo "Creating Dockerfile..."
  cat <<EOL > Dockerfile
# Use official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . ./

# Command to run the FastAPI application
CMD ["uvicorn", "app.main.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOL
  echo "Dockerfile created."
}

# Create directories
create_directories() {
  echo "Creating directory structure..."
  for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
      mkdir -p "$dir"
      echo "Created: $dir"
    else
      echo "Already exists: $dir"
    fi
  done
}

# Main function
main() {
  create_directories
  create_placeholder_files
}

# Execute main function from the root of the current directory
if [ "$(pwd)" != "$(git rev-parse --show-toplevel)" ]; then
  echo "Please run this script from the root of the repository directory."
  exit 1
fi

main

