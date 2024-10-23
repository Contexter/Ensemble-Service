# FountainAI Ensemble Service

This repository contains the implementation of the FountainAI Ensemble Service, a crucial component of the FountainAI system. The Ensemble Service acts as an intermediary between users, the OpenAI Assistant, and the various services managed via Kong API Gateway. It facilitates the orchestration and routing of user input across multiple services, following the mediator design pattern to ensure efficient delegation and aggregation of responses.

## Overview

The Ensemble Service is built using **FastAPI** and is defined according to the OpenAPI specification provided [here](https://github.com/Contexter/FountainAI/blob/main/openAPI/v4/Ensemble-Service.yml).

### Single User  and Multi User  Scenarios

For local, single-user use cases of FountainAI, an API Gateway is not required. The services can be accessed directly without  overhead . However, when FountainAI is scaled to a multi-user environment, an API Gateway ("Kong") becomes essential for managing and routing requests efficiently.

&#x20;A configuration switch will be introduced to allow toggling between local (single-user) and multi-user deployments.

## Project Structure

The project structure is organized as follows:

```
app/
  ├── prompt_factory/     # Manages system prompts for the Assistant.
  ├── interactions/       # Manages interaction flow.
  ├── logs/               # Stores logs for user inputs, responses, and interactions.
  ├── schemas/            # Stores JSON schemas for request and response validation.
  ├── main/               # Contains the main application entry point.
  ├── routers/            # Defines API routes.
  ├── models/             # Defines data models used by the application.
  ├── utils/              # Contains utility/helper functions.
  ├── config/             # Stores configuration files.
  ├── services/           # Contains business logic and service handlers.
  └── repositories/       # Manages data persistence and repository logic.
doc/                      # Stores the input OpenAPI specification.
Dockerfile                # Dockerfile for containerized deployment of the FastAPI application.
```

## Setup and Installation

To set up the FountainAI Ensemble Service locally, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Contexter/Ensemble-Service.git
   cd Ensemble-Service
   ```

2. **Run the setup script**:
   Use the provided setup script to create the directory structure and placeholder files for the FastAPI project:

   ```bash
   ./setup_fastapi_app_structure.sh
   ```

   This script will:

   - Create the necessary directories for different components of the FastAPI application.
   - Add placeholder `.gitkeep` files to ensure the directories are version-controlled.
   - Generate placeholder Python files and a `Dockerfile` for the project.

3. **Install dependencies**:
   Make sure you have Python installed. Create a virtual environment and install the required dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run the application**:
   Use `uvicorn` to run the FastAPI application locally:

   ```bash
   uvicorn app.main.main:app --host 0.0.0.0 --port 8000
   ```

## Deployment

The Ensemble Service is designed to be deployed using Docker. The `Dockerfile` created by the setup script can be used to build and run the application in a containerized environment.

### Docker Deployment Steps

1. **Build the Docker image**:

   ```bash
   docker build -t fountainai-ensemble-service .
   ```

2. **Run the Docker container**:

   ```bash
   docker run -p 8000:8000 fountainai-ensemble-service
   ```

### Docker Compose

All FountainAI services, including the Ensemble Service, are intended to be deployed using Docker Compose for simplified orchestration. The `docker-compose.yml` file will be provided to manage multiple services as part of the FountainAI system.

## References

- [FountainAI Ensemble Service OpenAPI Specification](https://github.com/Contexter/FountainAI/blob/main/openAPI/v4/Ensemble-Service.yml)

## Contributing

We welcome contributions! Please submit pull requests with clear descriptions of changes and reference any related issues.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

