# FountainAI Ensemble Service Development Plan (Dockerized Workflow)

## Introduction

This guide outlines a **specification-driven development strategy** for implementing the **FountainAI Ensemble Service** as a **FastAPI** application within a fully **Dockerized** local development environment. The FountainAI Ensemble Service is a core component of the FountainAI ecosystem, facilitating structured interactions between **users**, the **OpenAI Assistant SDK** (The Assistant), and various **FountainAI services**. It dynamically generates **system prompts** based on the **OpenAPI specifications** of each integrated FountainAI service.

Read its [OpenAPI Specification](https://github.com/Contexter/Ensemble-Service/blob/main/service/openapi3_1.yml).

## Project Organization and Script Management

To ensure a consistent and unambiguous **project structure**, the repository follows a standardized **folder layout** with a clear **root directory** and explicitly defined **paths**. The root directory of the project is `/service`.

### Updated Project Structure

```
/service
├── README.md
├── openapi3_1.yml
├── run_setup.sh
├── scripts/
│   ├── generate_dockerfile.py
│   ├── generate_docker_compose.py
│   ├── create_directory_structure.py
│   ├── generate_main_entry.py
│   ├── generate_schemas.py
│   ├── generate_authentication.py
│   ├── generate_models.py
│   ├── generate_alembic_migration.py
│   ├── generate_crud.py
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

- **Root Directory:** The root of the project is `/service`, with all paths relative to this root.
- **OpenAPI Specification:** The `openapi3_1.yml` file is located at the `/service` root directory.
- **Scripts Directory:** All **scripts** are housed within the `scripts/` directory at the root of the repository.
- **Application Code:** The `app/` directory contains the **FastAPI application code**, adhering to standard conventions.
- **Environment Variables:** Environment variables are utilized to define **base paths**, ensuring that scripts and code can adapt to different **execution contexts**, such as running inside versus outside **Docker**.
- **Path Definitions:** All paths within scripts are explicitly defined relative to the `/service` root directory to avoid ambiguity and ensure consistency.
- **Naming Conventions:** All scripts that generate or create files are prefixed with `generate_` for consistency. The Docker-related scripts are named `generate_dockerfile.py` and `generate_docker_compose.py` for clarity.

---

## Implementation Using Modular Scripts

### Overview

The development workflow utilizes **modular Python scripts** placed within the `/service/scripts/` directory. Each script performs a specific task, contributing to the overall setup of the FountainAI Ensemble Service. The `setup_fountainai_ensemble.py` script orchestrates the execution of all these scripts in the correct order.

Below is a detailed description of each script, including its purpose and the prompt that defines its functionality.

### 1. generate_dockerfile.py

**Description:**

This script generates a `Dockerfile` in the `/service` root directory, setting up the **Docker environment** with the necessary configurations for the **FastAPI application**.

**Prompt:**

> Generate a script named `generate_dockerfile.py` that will be placed in `/service/scripts/`. This script creates a `Dockerfile` in the `/service` root directory that uses an official Python base image (e.g., `python:3.11-slim`). It should set the working directory to `/service` to prevent recursive directory structures, install required system packages, copy the application code and scripts into the container ensuring files are placed correctly, install Python dependencies using `pip`, set environment variables as needed, and specify the command to run the **FastAPI application** using **Uvicorn**.

### 2. generate_docker_compose.py

**Description:**

This script generates a `docker-compose.yml` file in the `/service` root directory, defining the **services** required for the **FastAPI application** and **Typesense**, along with necessary configurations.

**Prompt:**

> Generate a script named `generate_docker_compose.py` that will be placed in `/service/scripts/`. This script creates a `docker-compose.yml` file in the `/service` root directory that defines services for the **FastAPI application** and **Typesense**. It should mount **volumes** to allow code changes to be reflected without rebuilding the image, expose necessary **ports**, set up **network configurations**, and include **environment variables** for development settings.

### 3. create_directory_structure.py

**Description:**

This script creates the necessary **directories** and **initial files** for the FountainAI Ensemble Service relative to the `/service` root directory, ensuring a minimal but functional **FastAPI application** setup.

**Prompt:**

> Generate a script named `create_directory_structure.py` that will be placed in `/service/scripts/`. This script creates the necessary **directories** and **initial files** for the FountainAI Ensemble Service relative to the `/service` root directory. It should create the following directories: `/service/app/`, `/service/app/api/routes/`, `/service/app/models/`, `/service/app/schemas/`, `/service/app/crud/`, `/service/app/core/`, `/service/app/auth/`, `/service/app/typesense/`, and `/service/app/tests/`. Additionally, it should create the **initial files**: `/service/app/main.py` with a basic FastAPI app instance, `/service/app/api/routes/__init__.py`, `/service/app/api/routes/root.py` with a root endpoint, and `__init__.py` files in each package as needed. The script should ensure that after execution, there is a minimal but functional FastAPI application that can be run and will respond to requests. It should print a **confirmation message** for each directory and file created. Ensure that the script is compatible with execution inside a Docker container and that all paths are explicitly defined relative to `/service`.

### 4. generate_main_entry.py

**Description:**

This script updates `/service/app/main.py` to include **routers**, **middleware**, **event handlers**, and any **global dependencies**, ensuring the application is ready to run with **Uvicorn**.

**Prompt:**

> Generate a script named `generate_main_entry.py` that will be placed in `/service/scripts/`. This script updates `/service/app/main.py` to include **routers** from `/service/app/api/routes/`, add **middleware**, **event handlers**, and any **global dependencies** as needed. It should ensure the application is ready to run with **Uvicorn**, overwrite any existing `main.py` file, and confirm upon completion. Ensure compatibility with Docker and that all paths are explicitly defined relative to `/service`.

### 5. generate_schemas.py

**Description:**

This script creates **Pydantic models** in `/service/app/schemas/` based on the schemas defined in the **OpenAPI specification**, ensuring they match exactly with **field types** and **validations**.

**Prompt:**

> Generate a script named `generate_schemas.py` that will be placed in `/service/scripts/`. This script creates **Pydantic models** in `/service/app/schemas/` corresponding to the schemas defined in the **OpenAPI specification** located at `/service/openapi3_1.yml`. It should ensure that the models match the specification exactly, including **field types** and **validations**. The script should generate separate files for each model as appropriate, overwrite any existing files, and provide a **confirmation message** upon completion. It should read the OpenAPI specification from the mounted volume inside the Docker container, referencing the path `/service/openapi3_1.yml`.

### 6. generate_authentication.py

**Description:**

This script creates **authentication dependencies** in `/service/app/auth/dependencies.py` based on the **OpenAPI specification**, implementing **API key authentication mechanisms**.

**Prompt:**

> Generate a script named `generate_authentication.py` that will be placed in `/service/scripts/`. This script creates `/service/app/auth/dependencies.py` with **authentication dependencies** as per the **OpenAPI specification** located at `/service/openapi3_1.yml`. It should implement the **API key authentication mechanisms** for both `apiKeyAuth` and `adminApiKeyAuth`, ensuring that the dependencies validate API keys correctly and raise appropriate **HTTP exceptions**. The script should overwrite any existing file and confirm upon completion. Ensure compatibility with Docker and that paths are explicitly defined relative to `/service`.

### 7. generate_models.py

**Description:**

This script generates **SQLAlchemy models** in `/service/app/models/` based on the **OpenAPI schemas**, ensuring accurate representation for **database use**.

**Prompt:**

> Generate a script named `generate_models.py` that will be placed in `/service/scripts/`. This script will create **SQLAlchemy models** in `/service/app/models/` corresponding to the **database schemas** defined in the **OpenAPI specification** located at `/service/openapi3_1.yml`. It should include necessary **relationships**, **field types**, **primary keys**, and **constraints**. The script should validate that each schema is suitable for generating a model, such as having valid class names. It should write each model into a separate Python file and create **backups** of existing files. Ensure compatibility with Docker by explicitly defining all paths relative to `/service`. Additionally, the script should **log progress** and **errors**, and report **tables created successfully** in the database.

### 8. generate_alembic_migration.py

**Description:**

This script sets up **Alembic** for the project and creates new **migrations** based on the current **SQLAlchemy models**, facilitating **database table creation** and **updates**.

**Prompt:**

> Generate a script named `generate_alembic_migration.py` that will be placed in `/service/scripts/`. This script should set up **Alembic** for the project if it is not already set up. It should create a new **Alembic migration** based on the current state of the **SQLAlchemy models** in `/service/app/models/` and place the migration files in `/service/migrations/`. Ensure that all paths are explicitly defined relative to `/service` and that the script is compatible with Docker. Additionally, it should **log the success or failure** of migration creation and any encountered issues.

### 9. generate_crud.py

**Description:**

This script generates **CRUD operation functions** in `/service/app/crud/` for the models created by the `generate_models.py` script, ensuring proper **session handling** and **exception management**.

**Prompt:**

> Generate a script named `generate_crud.py` that will be placed in `/service/scripts/`. This script will create **CRUD operation functions** in `/service/app/crud/` for the models generated by the `generate_models.py` script. It should define functions for **creating**, **reading**, **updating**, and **deleting records**, ensuring that each function properly handles **sessions** and **exceptions**. The script should write each model’s CRUD operations into a separate Python file, ensure that all paths are explicitly defined relative to `/service`, and are compatible with Docker. Additionally, it should include **error handling**, **logging**, and **validation** to ensure robustness.

### 10. generate_api_routes.py

**Description:**

This script creates **FastAPI route files** in `/service/app/api/routes/` based on the **OpenAPI specification**, including **route decorators** and **security dependencies**.

**Prompt:**

> Generate a script named `generate_api_routes.py` that will be placed in `/service/scripts/`. This script creates **route files** in `/service/app/api/routes/` with **FastAPI endpoints** as per the **OpenAPI specification** located at `/service/openapi3_1.yml`. For each endpoint, it should use the exact **path**, **HTTP method**, **parameters**, and **response models** defined in the specification. The script should add **route decorators** with `summary`, `description`, and `operation_id` to enhance the **OpenAPI documentation**, apply the appropriate **security dependencies** (`get_api_key`, `get_admin_api_key`), and include **error handling** and **response models** as specified. It should overwrite any existing route files and confirm upon completion. Ensure that the script is compatible with the **Dockerized environment** and that all paths are explicitly defined relative to `/service`.

### 11. generate_typesense_sync.py

**Description:**

This script sets up **Typesense client configuration** and **synchronization functions** in `/service/app/typesense/`, ensuring **data consistency** with **Typesense**.

**Prompt:**

> Generate a script named `generate_typesense_sync.py` that will be placed in `/service/scripts/`. This script should create `/service/app/typesense/client.py` with the **Typesense client configuration** and **synchronization functions** in `/service/app/typesense/` to keep the data in sync with Typesense. It should ensure that the **synchronization logic** includes **error handling** and **retries** as per the **OpenAPI specification** located at `/service/openapi3_1.yml`. The script should overwrite existing files and confirm upon completion. It should be designed to run within Docker, with all paths explicitly defined relative to `/service`.

### 12. generate_logging.py

**Description:**

This script sets up **logging configuration** and **middleware** in `/service/app/core/logging.py` to capture and log **interactions** as specified.

**Prompt:**

> Generate a script named `generate_logging.py` that will be placed in `/service/scripts/`. This script should create **logging configuration** in `/service/app/core/logging.py` and set up **middleware** or **dependency injection** for logging **requests** and **responses**. It should ensure that the logging setup captures **interactions** as specified in the **OpenAPI specification** located at `/service/openapi3_1.yml`. The script should overwrite existing files and confirm upon completion. Ensure compatibility with Docker and that all paths are explicitly defined relative to `/service`.

### 13. validate_openapi_schema.py

**Description:**

This script validates the generated **FastAPI OpenAPI schema** against the original **specification**, ensuring **consistency** and **accuracy**.

**Prompt:**

> Generate a script named `validate_openapi_schema.py` that will be placed in `/service/scripts/`. This script should start the **FastAPI application** within the script to generate the **OpenAPI schema**, load the original **OpenAPI specification** from `/service/openapi3_1.yml`, compare the generated schema with the original specification, and report any **discrepancies** in a clear and actionable manner. It should ensure the script is compatible with execution inside the Docker container and that all paths are explicitly defined relative to `/service`.

### 14. generate_tests.py

**Description:**

This script generates **pytest test cases** in `/service/app/tests/test_api.py` based on the **OpenAPI specification**, covering **valid requests**, **authentication**, and **error handling**.

**Prompt:**

> Generate a script named `generate_tests.py` that will be placed in `/service/scripts/`. This script should read the **OpenAPI specification** from `/service/openapi3_1.yml` and, for each **endpoint** defined in the specification, generate a **test case** using `pytest` that sends a request to the endpoint with **valid parameters**, checks that the **response status code** and **body** match the expected outputs defined in the specification, includes tests for **authentication mechanisms** validating that **unauthorized requests** are handled correctly, and handles **error cases** as defined in the specification. It should output the test cases to `/service/app/tests/test_api.py`, ensure the script is compatible with execution inside the Docker container, and that all paths are explicitly defined relative to `/service`.

### 15. setup_fountainai_ensemble.py

**Description:**

This master script executes all the previously generated Python scripts in the correct order to set up the **FountainAI Ensemble Service project**.

**Prompt:**

> Generate a script named `setup_fountainai_ensemble.py` that will be placed in `/service/scripts/`. This script should execute all the previously generated Python scripts in the correct order to set up the **FountainAI Ensemble Service project**. It should execute each Python script and check for **successful completion**, provide a final **confirmation message** upon successful setup, and ensure that the script is designed to run within the Docker container with all paths explicitly defined relative to `/service`.

### 16. run_setup.sh

**Description:**

This **shell script** automates the **Docker build** and **setup process** by building and starting the Docker containers and running the setup Python script within the container.

**Prompt:**

> Generate a shell script named `run_setup.sh` to be placed in `/service/`. This script should build and start the Docker containers using `docker-compose up --build -d`, wait for the containers to be ready, and then execute `python scripts/setup_fountainai_ensemble.py` inside the **FastAPI application** container. It should provide appropriate **echo statements** to inform the user of each step and ensure the script is **executable** and compatible with **Unix-based systems**.

---

## Notes on Workflow

### Prerequisites

- **Docker** and **Docker Compose** must be installed on your local machine.
- Refer to the [Docker installation guide](https://docs.docker.com/get-docker/) for detailed instructions.

### Clone the Repository

Clone the repository and navigate to the `/service` directory:

```bash
git clone https://github.com/Contexter/Ensemble-Service.git
cd Ensemble-Service/service
```

### Configure the Docker Environment

Use the `generate_dockerfile.py` and `generate_docker_compose.py` scripts to create the `Dockerfile` and `docker-compose.yml` in the `/service` root directory.

```bash
python scripts/generate_dockerfile.py
python scripts/generate_docker_compose.py
```

Ensure that the Docker configurations are set up to support a seamless **local development workflow**.

### Build and Start the Docker Environment

Use the generated `run_setup.sh` script to automate the setup process:

```bash
chmod +x run_setup.sh
./run_setup.sh
```

This command will:

- Build the Docker image for the **FastAPI application**.
- Start the **FastAPI application** and **Typesense services**.
- Execute the `setup_fountainai_ensemble.py` script inside the Docker container to set up the project.

### Develop and Test

With the **Docker environment** running, you can engage in development and testing activities. **Editing code locally** will reflect changes inside the container due to **volume mounting**.

- **Access the application** by visiting [http://localhost:8000](http://localhost:8000).
- **Run tests inside the container**:

  ```bash
  docker-compose exec app bash
  pytest
  ```

The application should be fully functional after running the initial scripts, including the basic **FastAPI app** created by `create_directory_structure.py`.

### Shut Down the Environment

When development is complete, you can stop the Docker containers with:

```bash
docker-compose down
```

### Notes on Volume Mounting and Environment Variables

#### Volume Mounting

The `docker-compose.yml` file is configured to **mount your local project directory** into the Docker container. This setup allows you to make changes locally and have them take effect inside the container without the need to rebuild the Docker image each time.

#### Environment Variables

Manage **environment variables** using a `.env` file to maintain development settings. It is crucial to ensure that **sensitive information** is not committed to **version control systems** to maintain security.

---

## License

This project is licensed under the terms of the **MIT license**.

Please feel free to contribute to this project by submitting **issues** or **pull requests**. If you have any questions or need further assistance, don’t hesitate to reach out!

---

## Appendix: Keyword Index

### Technologies and Tools

| **Keyword**         | **Description**                                                                                                                                                              |
|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Docker**          | A platform that uses OS-level virtualization to deliver software in packages called containers, ensuring consistency across environments.                                     |
| **Docker Compose**  | A tool for defining and running multi-container Docker applications, allowing services to be managed collectively.                                                            |
| **FastAPI**         | A modern, fast (high-performance) web framework for building APIs with Python based on standard Python type hints.                                                            |
| **Alembic**         | A lightweight database migration tool for use with SQLAlchemy, enabling version control for database schemas.                                                                |
| **SQLAlchemy**      | An SQL toolkit and ORM for Python, facilitating database interactions.                                                                                                       |
| **Pydantic models** | Data validation and settings management using Python type annotations, used in FastAPI to define the shape of request and response data.                                     |
| **Uvicorn**         | A lightning-fast ASGI server implementation, used to serve FastAPI applications in production environments.                                                                   |
| **Typesense**       | An open-source, fast, typo-tolerant search engine optimized for instant search-as-you-type experiences, used for data synchronization and search functionalities.             |

### Security

| **Keyword**                | **Description**                                                                                                                                                         |
|----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **API key authentication** | A security mechanism that uses unique keys to authenticate requests to the API, ensuring that only authorized users can access certain endpoints.                       |

### Development Practices

| **Keyword**              | **Description**                                                                                                                                                   |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Code integration**     | The process of combining different pieces of code and ensuring they work together seamlessly within the application.                                              |
| **Version control**      | Systems like Git that track changes in code over time, facilitating collaboration and maintaining the history of the project.                                     |
| **Testing and validation** | The process of verifying that the application works as intended and meets the defined specifications through automated tests and schema validation.             |

### Components

| **Keyword**            | **Description**                                                                                                                                                      |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **CRUD operations**    | The basic operations of Create, Read, Update, and Delete, essential for managing data within the application.                                                        |
| **Route decorators**   | Annotations in FastAPI that define the behavior of API endpoints, including metadata like summaries, descriptions, and operation IDs to enhance documentation.        |
| **Logging configuration** | The setup that determines how and where application logs are recorded, ensuring that important interactions and errors are tracked.                             |
| **Modular scripts**    | Separate, reusable Python scripts that handle specific tasks within the development workflow, promoting code reusability and maintainability.                       |

### Concepts

| **Keyword**               | **Description**                                                                                                                                                                |
|---------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Environment variables** | Variables that are set outside of the application code and used to configure the application's behavior in different environments (e.g., development, production).              |
| **Volume mounting**       | A Docker feature that allows directories from the host machine to be mounted into containers, enabling live code changes without rebuilding images.                            |
| **OpenAPI specification** | A standard, language-agnostic interface to RESTful APIs that allows both humans and computers to understand the capabilities of a service without accessing its source code.    |
| **Schema generation**     | The automatic creation of API schemas based on defined models and routes, ensuring consistency between the application and its documentation.                                   |

### Data Management

| **Keyword**          | **Description**                                                                                                                                                           |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Data persistence** | The storage of data in a way that it remains available and intact across application restarts and failures.                                                               |
| **SQLite**           | A lightweight, disk-based database that doesn't require a separate server process, used for data persistence.                                                              |
| **Synchronization**  | The process of ensuring that data remains consistent across different systems or components, such as between a database and a search engine.                               |

### User Interaction

| **Keyword**              | **Description**                                                                                                                                              |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **System prompts**       | Predefined messages or instructions generated based on the OpenAPI specifications to guide the interactions between users and the assistant.                 |
| **Interacting services** | External or internal services that the FountainAI Ensemble Service communicates with to perform various tasks or retrieve data.                               |

---

## Summary

By following this guide, you will set up a fully Dockerized development environment for the FountainAI Ensemble Service, leveraging modular scripts to automate the creation of the application structure, configurations, and components based on the provided OpenAPI specification. This approach ensures consistency, scalability, and ease of maintenance, aligning with best practices in modern software development.