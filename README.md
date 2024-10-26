# FountainAI Ensemble Service Development Plan (Dockerized Workflow)

![The FountainAI Ensemble Service](https://coach.benedikt-eickhoff.de/koken/storage/cache/images/000/738/Ensemble-Service,xlarge.1729067517.png)

## Introduction

The **FountainAI Ensemble Service** is a core component of the **FountainAI ecosystem**, facilitating structured interactions between users, the **OpenAI Assistant SDK (The Assistant)**, and various **FountainAI services**. It dynamically generates system prompts based on the OpenAPI specifications of each integrated service.

This README outlines a **specification-driven development strategy** for implementing the FountainAI Ensemble Service FastAPI application, ensuring an exact match between the OpenAPI specification and the FastAPI implementation. The approach leverages **modular scripts** and a **fully Dockerized local development environment** to automate code generation and integration.

By setting up Docker at the very beginning, we ensure a consistent, reliable, and efficient environment for building and testing the FountainAI Ensemble Service from the ground up.

## Table of Contents

- [Objectives and Scope](#objectives-and-scope)
- [Specification-Driven Development Strategy](#specification-driven-development-strategy)
- [Implementation Plan Using Modular Scripts](#implementation-plan-using-modular-scripts)
- [Dockerized Local Development Workflow](#dockerized-local-development-workflow)
- [Next Steps](#next-steps)
- [License](#license)

---

## Objectives and Scope

### Key Objectives

- **Dockerized Environment Setup**: Establish the Docker environment at the very beginning to manage the local development environment and eliminate Python environment issues.
- **Specification-Driven Development**: Implement the FastAPI application to exactly match the OpenAPI specification.
- **Automated Code Integration**: Use modular scripts to automate the creation and updating of project files and directories within the Docker environment.
- **System Prompt Generation**: Generate system prompts using OpenAPI definitions.
- **Service Interaction Management**: Orchestrate interactions between users, the Assistant, and services.
- **Interaction Logging**: Log interactions for transparency and traceability.
- **Data Persistence and Synchronization**: Use SQLite for persistence and synchronize with Typesense.
- **API Security**: Implement API key authentication.
- **Service Management**: Provide administrative endpoints for managing the service registry.

### Scope of the Service

Designed for both local deployment (testing and development) and cloud-based operations, the service manages queries, processes responses, coordinates service interactions, and allows for easy updates as new services are added.

---

## Specification-Driven Development Strategy

### Project Organization and Script Management

To ensure a consistent and unambiguous project structure, the repository will follow a standardized folder structure, with a clear root directory and all paths explicitly defined. The root directory of the project will be `/service`.

#### Updated Project Structure

```
/service
├── README.md
├── openapi3_1.yml
├── docker-compose.yml
├── Dockerfile
├── scripts/
│   ├── create_directory_structure.py
│   ├── generate_main_entry.py
│   ├── generate_schemas.py
│   ├── generate_authentication.py
│   ├── generate_models_and_crud.py
│   ├── generate_api_routes.py
│   ├── generate_typesense_sync.py
│   ├── generate_logging.py
│   ├── validate_openapi_schema.py
│   ├── generate_tests.py
│   ├── setup_fountainai_ensemble.py
│   └── ...
└── app/
    ├── api/
    │   └── routes/
    ├── auth/
    ├── core/
    ├── crud/
    ├── models/
    ├── schemas/
    ├── typesense/
    ├── main.py
    ├── tests/
    └── ...
```

**Notes:**

- The root of the project is `/service`. All paths are relative to this root.
- The `openapi3_1.yml` file resides at the `/service` root, separate from FastAPI's `app` directory, to prevent conflicts between manually defined OpenAPI specs and FastAPI-generated ones.
- All scripts are placed inside the `scripts/` directory at the root of the repository.
- The `app/` directory contains the FastAPI application code, following standard conventions.

#### Path Adaptation Based on Environment

- Use environment variables to define base paths, ensuring that scripts and code can adapt to different execution contexts (e.g., inside vs. outside Docker).
- All paths within scripts should be explicitly defined relative to the `/service` root directory to avoid ambiguity and ensure consistency.

#### Instructions for Running Scripts

- All scripts will be executed within Docker containers to ensure a consistent environment.
- From the root directory of the repository, you can build and run the Docker environment using Docker Compose:

  ```sh
  docker-compose up --build
  ```

- The `setup_fountainai_ensemble.py` script will be executed within the Docker container to perform initial setup tasks.

### Overview

The development strategy is centered around using the **OpenAPI specification** as the **single source of truth**, ensuring that the FastAPI implementation matches it exactly. This includes:

- Generating Pydantic models directly from the OpenAPI schemas.
- Implementing API endpoints with paths, methods, parameters, and responses exactly as defined.
- Overwriting FastAPI's default behavior by explicitly setting `operationId`, `summary`, and `description` in the route decorators.
- Using FastAPI's capabilities to generate the OpenAPI schema and validating it against the original specification.
- Automating code generation and integration using modular scripts within a Dockerized environment.

**Note**: The OpenAPI specification resides in this repository at `openapi3_1.yml` in the `/service` root directory. This file should be referred to when implementing the application to ensure consistency and accuracy.

---

## Implementation Plan Using Modular Scripts

The implementation plan focuses on translating the OpenAPI specification into an exact FastAPI implementation, automating code generation and integration using modular scripts within a Dockerized environment. The steps are ordered to facilitate a smooth development process, starting with setting up Docker.

### Step 1: Configure the Docker Environment

**Objective**: Set up Docker and Docker Compose configurations to manage the local development environment from the outset, ensuring files are correctly placed and paths are consistent.

**Actions**:

- **Dockerfile**:

  - Create a `Dockerfile` in the `/service` root directory that:

    - Uses an official Python base image (e.g., `python:3.11-slim`).
    - Sets the working directory to `/service` to prevent recursive directory structures.
    - Installs required system packages.
    - Copies the application code and scripts into the container, ensuring files are placed correctly.
    - Installs Python dependencies using `pip`.
    - Sets environment variables as needed.
    - Specifies the command to run the FastAPI application using Uvicorn.

- **docker-compose.yml**:

  - Create a `docker-compose.yml` file in the `/service` root directory that:

    - Defines services for the FastAPI application and Typesense.
    - Mounts volumes to allow code changes to be reflected without rebuilding the image.
    - Exposes necessary ports.
    - Sets up network configurations.
    - Includes environment variables for development settings.

- **Advantages of Early Docker Setup**:

  - **Consistent Development Environment**: Setting up Docker first ensures that all development occurs in a consistent environment, preventing issues related to differing local configurations.
  - **Dependency Isolation**: Dependencies are managed within the Docker container, avoiding conflicts with other projects or system-wide packages.
  - **Simplifies Onboarding**: New team members can get the project up and running quickly without dealing with complex environment setups.
  - **Streamlines Development Workflow**: By working within Docker from the outset, developers can leverage Docker's features such as volume mounting, environment variable management, and networking.
  - **Early Detection of Issues**: Setting up Docker early helps identify any compatibility issues with the containerization process before significant development effort is invested.

- **Best Practices for Dockerized Development**:

  - **Use Official Base Images**: Start from official Python images to ensure security and compatibility.
  - **Leverage Docker Compose**: Use Docker Compose to manage multi-container applications and simplify commands.
  - **Avoid Hardcoding Configuration**: Use environment variables and configuration files to manage settings.
  - **Keep Images Lean**: Use slim or alpine versions of base images and clean up unnecessary files to reduce image size.
  - **Automate as Much as Possible**: Use scripts and Docker features to automate setup, testing, and deployment processes.

- **Functional Prompt**:

  ```
  Generate a Dockerfile in the `/service` root directory to containerize the FastAPI application, ensuring that it includes all necessary dependencies and copies the application code into the container without creating nested directories. Use `/service` as the working directory to prevent recursive structures. Also, generate a `docker-compose.yml` file in the `/service` root directory to orchestrate the application and its dependencies, such as Typesense. Ensure that the Docker configurations match the project's requirements, including necessary environment variables. The configurations should support a local development workflow and ensure that both development and containerized environments are consistent.
  ```

### Step 2: Prepare the OpenAPI Specification

**Objective**: Ensure you have a comprehensive and finalized OpenAPI specification (`openapi3_1.yml`) that serves as the single source of truth, placed at the `/service` root directory.

**Actions**:

- Review and validate the OpenAPI specification to include all endpoints, schemas, security schemes, and descriptions.
- Confirm that `operationId`, `summary`, and `description` are explicitly defined for each endpoint to overwrite FastAPI's default behavior.
- Ensure the `openapi3_1.yml` file is located at `/service/openapi3_1.yml`.

### Step 3: Define Modular Components and Functional Prompts

**Objective**: Break down the project into modular components and create functional prompts that instruct GPT-4 to generate the content of the named scripts, ensuring compatibility with a Dockerized environment and consistent file placement.

**Actions**:

For each script, explicitly define the input and output paths relative to the `/service` root directory, and include these details in the GPT prompts.

1. **Directory Structure and Initial FastAPI Setup**

   - **Functional Prompt**:

     ```
     Generate a script named `create_directory_structure.py` that will be placed in `/service/scripts/`. This script creates the necessary directories and initial files for the FountainAI Ensemble Service relative to the `/service` root directory, including:

     **Directories:**

     - `/service/app/`
     - `/service/app/api/routes/`
     - `/service/app/models/`
     - `/service/app/schemas/`
     - `/service/app/crud/`
     - `/service/app/core/`
     - `/service/app/auth/`
     - `/service/app/typesense/`
     - `/service/app/tests/`

     **Initial Files:**

     - `/service/app/main.py` with a basic FastAPI app instance.
     - `/service/app/api/routes/__init__.py`
     - `/service/app/api/routes/root.py` with a root endpoint.
     - `__init__.py` files in each package as needed.

     The script should ensure that after execution, there is a minimal but functional FastAPI application that can be run and will respond to requests. The script should print a confirmation message for each directory and file created. Ensure that the script is compatible with execution inside a Docker container and that all paths are explicitly defined relative to `/service`.
     ```

2. **Main Application Entry Point**

   - **Functional Prompt**:

     ```
     Generate a script named `generate_main_entry.py` that will be placed in `/service/scripts/`. This script updates `/service/app/main.py` to:

     - Include routers from `/service/app/api/routes/`.
     - Set the custom OpenAPI schema by loading `/service/openapi3_1.yml` to ensure the application's OpenAPI schema matches the specification exactly.
     - Overwrite any existing `main.py` file and confirm upon completion.
     - Ensure compatibility with Docker and that all paths are explicitly defined relative to `/service`.
     ```

3. **Pydantic Models (Schemas)**

   - **Functional Prompt**:

     ```
     Generate a script named `generate_schemas.py` that will be placed in `/service/scripts/`. This script creates `/service/app/schemas/models.py` with Pydantic models corresponding to the schemas defined in the OpenAPI specification located at `/service/openapi3_1.yml`. Ensure that the models match the specification exactly, including field types and validations. The script should overwrite any existing `models.py` file and provide a confirmation message upon completion. The script should read the OpenAPI specification from the mounted volume inside the Docker container, referencing the path `/service/openapi3_1.yml`.
     ```

4. **Authentication Dependencies**

   - **Functional Prompt**:

     ```
     Generate a script named `generate_authentication.py` that will be placed in `/service/scripts/`. This script creates `/service/app/auth/dependencies.py` with authentication dependencies as per the OpenAPI specification located at `/service/openapi3_1.yml`. Implement the API key authentication mechanisms for both `apiKeyAuth` and `adminApiKeyAuth`. The script should ensure that the dependencies validate API keys correctly and raise appropriate HTTP exceptions. Overwrite any existing file and confirm upon completion. Ensure compatibility with Docker and that paths are explicitly defined relative to `/service`.
     ```

5. **Database Models and CRUD Operations**

   - **Functional Prompt**:

     ```
     Generate a script named `generate_models_and_crud.py` that will be placed in `/service/scripts/`. This script creates:

     - `/service/app/models/service.py` with SQLAlchemy models corresponding to the service registry.
     - `/service/app/crud/service.py` with CRUD operations for the service registry.

     Ensure that the database models match the Pydantic models and the OpenAPI schemas located at `/service/openapi3_1.yml`. Include necessary relationships and field types. The script should overwrite existing files and confirm upon completion. The script should be designed to run inside the Docker environment, and all paths should be explicitly defined relative to `/service`.
     ```

6. **API Routes (Endpoints)**

   - **Functional Prompt**:

     ```
     Generate a script named `generate_api_routes.py` that will be placed in `/service/scripts/`. This script creates `/service/app/api/routes/services.py` with FastAPI endpoints as per the OpenAPI specification located at `/service/openapi3_1.yml`. For each endpoint:

     - Use the exact path, HTTP method, parameters, and response models defined in the specification.
     - Explicitly set `operationId`, `summary`, and `description` in the route decorators to overwrite FastAPI's default behavior.
     - Apply the appropriate security dependencies (`get_api_key`, `get_admin_api_key`).
     - Include error handling and response models as specified.
     - The script should overwrite any existing `services.py` file and confirm upon completion. Ensure that the script is compatible with the Dockerized environment and that all paths are explicitly defined relative to `/service`.
     ```

7. **Typesense Synchronization**

   - **Functional Prompt**:

     ```
     Generate a script named `generate_typesense_sync.py` that will be placed in `/service/scripts/`. This script creates:

     - `/service/app/typesense/client.py` with the Typesense client configuration.
     - `/service/app/typesense/service_sync.py` with functions to synchronize the service registry with Typesense.

     Ensure that the synchronization logic includes error handling and retries as per the OpenAPI specification located at `/service/openapi3_1.yml`. The script should overwrite existing files and confirm upon completion. The script should be designed to run within Docker, and all paths should be explicitly defined relative to `/service`.
     ```

8. **Logging Setup**

   - **Functional Prompt**:

     ```
     Generate a script named `generate_logging.py` that will be placed in `/service/scripts/`. This script creates:

     - `/service/app/models/log.py` with database models for logging interactions.
     - `/service/app/crud/log.py` with CRUD operations for logs.
     - `/service/app/typesense/log_sync.py` with functions to synchronize logs with Typesense.

     Ensure that the logging models and operations match the OpenAPI specification located at `/service/openapi3_1.yml`. The script should overwrite existing files and confirm upon completion. Ensure compatibility with Docker and that all paths are explicitly defined relative to `/service`.
     ```

9. **Validation Script**

   - **Functional Prompt**:

     ```
     Generate a script named `validate_openapi_schema.py` that will be placed in `/service/scripts/`. This script should:

     - Start the FastAPI application within the script to generate the OpenAPI schema.
     - Load the original OpenAPI specification from `/service/openapi3_1.yml`.
     - Compare the generated schema with the original specification.
     - Report any discrepancies in a clear and actionable manner.
     - Ensure the script is compatible with execution inside the Docker container and that all paths are explicitly defined relative to `/service`.
     ```

10. **Test Generation Script**

    - **Functional Prompt**:

      ```
      Generate a script named `generate_tests.py` that will be placed in `/service/scripts/`. This script should:

      - Read the OpenAPI specification from `/service/openapi3_1.yml`.
      - For each endpoint defined in the specification, generate a test case using `pytest` that:

        - Sends a request to the endpoint with valid parameters.
        - Checks that the response status code and body match the expected outputs defined in the specification.
        - Includes tests for authentication mechanisms, validating that unauthorized requests are handled correctly.
        - Handles error cases as defined in the specification.

      - Output the test cases to `/service/app/tests/test_api.py`.
      - Ensure the script is compatible with execution inside the Docker container and that all paths are explicitly defined relative to `/service`.
      ```

11. **Master Script**

    - **Functional Prompt**:

      ```
      Generate a script named `setup_fountainai_ensemble.py` that will be placed in `/service/scripts/`. This script executes all the previously generated Python scripts in the correct order to set up the FountainAI Ensemble Service project. The script should:

      - Execute each Python script and check for successful completion.
      - Provide a final confirmation message upon successful setup.
      - The script should be designed to run within the Docker container, and all paths should be explicitly defined relative to `/service`.
      ```

12. **Automation Shell Script**

    - **Functional Prompt**:

      ```
      Generate a shell script named `run_setup.sh` to be placed in `/service/`. This script should:

      - Build and start the Docker containers using `docker-compose up --build`.
      - Access the FastAPI application container's shell and run the setup script `python scripts/setup_fountainai_ensemble.py`.
      - Provide appropriate echo statements to inform the user of each step.
      - Ensure the script is executable and compatible with Unix-based systems.
      ```

---

### Step 4: Execute Scripts Within Docker Containers

**Objective**: Run the generated Python scripts within the Docker environment to build or update your local project from the beginning.

**Actions**:

- Use the generated `run_setup.sh` script to automate the setup process:

  ```sh
  chmod +x run_setup.sh
  ./run_setup.sh
  ```

- **Clarification of Script Roles**:

  - **`setup_fountainai_ensemble.py`**: This script runs inside the Docker container and executes all the other Python scripts to set up the application.
  - **`run_setup.sh`**: This shell script runs on the host machine to automate building the Docker image, starting the container, and executing `setup_fountainai_ensemble.py`.

### Step 5: Validate FastAPI Implementation Against OpenAPI Specification

**Objective**: Ensure that the FastAPI application matches the OpenAPI specification exactly, not relying solely on automatic OpenAPI generation capabilities.

**Actions**:

- Use the `validate_openapi_schema.py` script generated in **Step 3** to compare the application's OpenAPI schema with the original specification:

  ```sh
  docker-compose exec app bash
  cd /service
  python scripts/validate_openapi_schema.py
  ```

- Review any discrepancies reported by the script and make necessary adjustments.

### Step 6: Testing and Validation

**Objective**: Test the application to ensure it functions as expected and matches the OpenAPI specification.

**Actions**:

- Use the `generate_tests.py` script generated in **Step 3** to create test cases based on the OpenAPI specification:

  ```sh
  docker-compose exec app bash
  cd /service
  python scripts/generate_tests.py
  ```

- Run the generated tests using `pytest`:

  ```sh
  pytest
  ```

- Ensure that all tests pass, indicating that the implementation aligns with the specification.

---

## Dockerized Local Development Workflow

### Advantages of Setting Up Docker First

- **Eliminates Environment Inconsistencies**: By establishing Docker from the beginning, all development occurs within a consistent environment.
- **Simplifies Dependency Management**: Dependencies are managed within the Docker container, avoiding conflicts with local Python environments.
- **Eases Onboarding**: New developers can start working on the project without complex setup procedures.
- **Facilitates Testing and Deployment**: The same Docker setup can be used in all stages of development and deployment.
- **Early Detection of Issues**: Setting up Docker early helps identify any compatibility issues with the containerization process before significant development effort is invested.

### Workflow Steps

1. **Install Docker and Docker Compose**

   - Ensure that Docker and Docker Compose are installed on your local machine.
   - Refer to the [Docker installation guide](https://docs.docker.com/get-docker/) for instructions.

2. **Clone the Repository**

   ```sh
   git clone https://github.com/Contexter/Ensemble-Service.git
   cd Ensemble-Service/service
   ```

3. **Configure the Docker Environment**

   - Create the `Dockerfile` and `docker-compose.yml` in the `/service` root directory as per the functional prompts.
   - Ensure that the Docker configurations support a local development workflow.

4. **Build and Start the Docker Environment**

   - Use the generated `run_setup.sh` script to automate the setup:

     ```sh
     chmod +x run_setup.sh
     ./run_setup.sh
     ```

     - This command will:

       - Build the Docker image for the FastAPI application.
       - Start the FastAPI application and Typesense services.
       - Execute the `setup_fountainai_ensemble.py` script inside the Docker container to set up the project.

5. **Develop and Test**

   - With the Docker environment running, you can:

     - Edit code locally, and changes will be reflected inside the container due to volume mounting.
     - Access the application at `http://localhost:8000`.
     - Run tests inside the container:

       ```sh
       docker-compose exec app bash
       pytest
       ```

     - The application should be functional after running the initial scripts, including the basic FastAPI app created in `create_directory_structure.py`.

6. **Shut Down the Environment**

   - When you're done, you can stop the containers:

     ```sh
     docker-compose down
     ```

### Notes on Volume Mounting and Environment Variables

- **Volume Mounting**:

  - The `docker-compose.yml` file is configured to mount your local project directory into the Docker container. This allows you to make changes locally and have them take effect inside the container without rebuilding the image.

- **Environment Variables**:

  - Use a `.env` file to manage environment variables for development.
  - Ensure that sensitive information is not committed to version control.

---

## Next Steps

- **Initiate a GPT-4 session**, providing the functional prompts to generate the Docker configurations and Python scripts, ensuring they are compatible with execution inside Docker, and that all paths are explicitly defined relative to `/service`.
- **Configure the Docker environment** by creating the `Dockerfile` and `docker-compose.yml` in the `/service` root directory as per the prompts, before any other implementation steps.
- **Execute the Python scripts** within the Docker container to set up the project.
- **Validate the FastAPI implementation** against the OpenAPI specification using the `validate_openapi_schema.py` script.
- **Write and run tests** inside the Docker container using the `generate_tests.py` script to verify the application's functionality.
- **Use version control** to track changes and facilitate collaboration.

---

## License

This project is licensed under the terms of the MIT license.

---

Please feel free to contribute to this project by submitting issues or pull requests. If you have any questions or need further assistance, don't hesitate to reach out!

---

This rewritten guide incorporates the recommended changes to remove redundancies and improve clarity, ensuring a streamlined and efficient development process.
