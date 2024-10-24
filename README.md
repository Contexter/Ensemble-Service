# FountainAI Ensemble Service Development Plan

![The FountainAI Ensemble Service]\(https\://coach.benedikt-eickhoff.de/koken/storage/cache/images/000/738/Ensemble-Service,xlarge.1729067517.png)

## Introduction

The **FountainAI Ensemble Service** is a core component of the **FountainAI ecosystem**, facilitating structured interactions between users, the **OpenAI Assistant SDK (The Assistant)**, and various **FountainAI services**. It dynamically generates system prompts based on the OpenAPI specifications of each integrated service.

This README outlines a **specification-driven development strategy** for implementing the FountainAI Ensemble Service FastAPI application, ensuring an exact match between the OpenAPI specification and the FastAPI implementation. The approach leverages **modular scripts** to automate code generation and integration into the local development environment.

## Table of Contents

- [Objectives and Scope](#objectives-and-scope)
- [Specification-Driven Development Strategy](#specification-driven-development-strategy)
- [Implementation Plan Using Modular Scripts](#implementation-plan-using-modular-scripts)
- [Next Steps](#next-steps)
- [License](#license)

---

## Objectives and Scope

### Key Objectives

- **Specification-Driven Development**: Implement the FastAPI application to exactly match the OpenAPI specification.
- **Automated Code Integration**: Use modular scripts to automate the creation and updating of project files and directories.
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

To keep the repository tidy and conventional, a dedicated `scripts/` directory will be created at the root of the repository. All setup and utility scripts will be placed inside this `scripts/` directory. This ensures a clean project structure where non-core files are separated logically.

#### Updated Project Structure

```
.
├── README.md
├── openapi3_1.yml
├── reset_main_branch.sh
├── scripts/
│   ├── create_directory_structure.py
│   ├── generate_schemas.py
│   ├── generate_authentication.py
│   └── ...
└── app/
    ├── api/
    ├── models/
    ├── ...
```

#### Instructions for Running Scripts

- From the root directory of the repository, utility scripts can be run using the following command:
  ```sh
  python scripts/create_directory_structure.py
  ```
- A master script (e.g., `setup_fountainai_ensemble.py`) will be added inside the `scripts/` directory to sequentially execute all setup tasks.

### Overview

The development strategy is centered around using the **OpenAPI specification** as the **single source of truth**, ensuring that the FastAPI implementation matches it exactly. This includes:

- Generating Pydantic models directly from the OpenAPI schemas.
- Implementing API endpoints with paths, methods, parameters, and responses exactly as defined.
- Overwriting FastAPI's default behavior by explicitly setting `operationId`, `summary`, and `description` in the route decorators.
- Using FastAPI's capabilities to generate the OpenAPI schema and validating it against the original specification.
- Automating code generation and integration using modular scripts.

**Note**: The OpenAPI specification resides in this repository at [`openapi3_1.yml`](https://github.com/Contexter/Ensemble-Service/blob/main/openapi3_1.yml). This file should be referred to when implementing the application to ensure consistency and accuracy.

---

## Implementation Plan Using Modular Scripts

The implementation plan focuses on translating the OpenAPI specification into an exact FastAPI implementation, automating code generation and integration using modular scripts. The steps are ordered intuitively to facilitate a smooth development process.

### Step 1: Prepare the OpenAPI Specification

**Objective**: Ensure you have a comprehensive and finalized OpenAPI specification (`openapi3_1.yml`) that serves as the single source of truth.

**Actions**:

- Review and validate the OpenAPI specification to include all endpoints, schemas, security schemes, and descriptions.
- Confirm that `operationId`, `summary`, and `description` are explicitly defined for each endpoint to overwrite FastAPI's default behavior.
- **Access the OpenAPI specification at the absolute link**: [`openapi3_1.yml`](https://github.com/Contexter/Ensemble-Service/blob/main/openapi3_1.yml).

### Step 2: Define Modular Components and Functional Prompts

**Objective**: Break down the project into modular components and create functional prompts that instruct GPT-4 to generate the content of the named scripts.

**Actions**:

1. **Directory Structure**

   - **Functional Prompt**:
     ```
     Generate a script named `create_directory_structure.py` that creates the necessary directories for the FountainAI Ensemble Service, including `app/`, `app/api/routes/`, `app/models/`, `app/schemas/`, `app/crud/`, `app/core/`, `app/auth/`, `app/typesense/`, and `app/tests/`. The script should print a confirmation message for each directory created.
     ```

2. **Pydantic Models (Schemas)**

   - **Functional Prompt**:
     ```
     Generate a script named `generate_schemas.py` that creates `app/schemas/models.py` with Pydantic models corresponding to the schemas defined in the OpenAPI specification (`openapi3_1.yml`). Ensure that the models match the specification exactly, including field types and validations. The script should overwrite any existing `models.py` file and provide a confirmation message upon completion.
     ```

3. **Authentication Dependencies**

   - **Functional Prompt**:
     ```
     Generate a script named `generate_authentication.py` that creates `app/auth/dependencies.py` with authentication dependencies as per the OpenAPI specification (`openapi3_1.yml`). Implement the API key authentication mechanisms for both `apiKeyAuth` and `adminApiKeyAuth`. The script should ensure that the dependencies validate API keys correctly and raise appropriate HTTP exceptions. Overwrite any existing file and confirm upon completion.
     ```

4. **Database Models and CRUD Operations**

   - **Functional Prompt**:
     ```
     Generate a script named `generate_models_and_crud.py` that creates:

     - `app/models/service.py` with SQLAlchemy models corresponding to the service registry.
     - `app/crud/service.py` with CRUD operations for the service registry.

     Ensure that the database models match the Pydantic models and the OpenAPI schemas (`openapi3_1.yml`). Include necessary relationships and field types. The script should overwrite existing files and confirm upon completion.
     ```

5. **API Routes (Endpoints)**

   - **Functional Prompt**:
     ```
     Generate a script named `generate_api_routes.py` that creates `app/api/routes/services.py` with FastAPI endpoints as per the OpenAPI specification (`openapi3_1.yml`). For each endpoint:

     - Use the exact path, HTTP method, parameters, and response models defined in the specification.
     - Explicitly set `operationId`, `summary`, and `description` in the route decorators to overwrite FastAPI's default behavior.
     - Apply the appropriate security dependencies (`get_api_key`, `get_admin_api_key`).
     - Include error handling and response models as specified.
     - The script should overwrite any existing `services.py` file and confirm upon completion.
     ```

6. **Typesense Synchronization**

   - **Functional Prompt**:
     ```
     Generate a script named `generate_typesense_sync.py` that creates:

     - `app/typesense/client.py` with the Typesense client configuration.
     - `app/typesense/service_sync.py` with functions to synchronize the service registry with Typesense.

     Ensure that the synchronization logic includes error handling and retries as per the OpenAPI specification (`openapi3_1.yml`). The script should overwrite existing files and confirm upon completion.
     ```

7. **Logging Setup**

   - **Functional Prompt**:
     ```
     Generate a script named `generate_logging.py` that creates:

     - `app/models/log.py` with database models for logging interactions.
     - `app/crud/log.py` with CRUD operations for logs.
     - `app/typesense/log_sync.py` with functions to synchronize logs with Typesense.

     Ensure that the logging models and operations match the OpenAPI specification (`openapi3_1.yml`). The script should overwrite existing files and confirm upon completion.
     ```

8. **Main Application Entry Point**

   - **Functional Prompt**:
     ```
     Generate a script named `generate_main_entry.py` that creates `app/main.py`. The script should:

     - Initialize the FastAPI application.
     - Include routers from `app/api/routes/`.
     - Set the custom OpenAPI schema by loading `openapi3_1.yml` to ensure the application's OpenAPI schema matches the specification exactly.
     - The script should overwrite any existing `main.py` file and confirm upon completion.
     ```

9. **Dockerfile and Docker Compose Configuration**

   - **Functional Prompt**:
     ```
     Generate a script named `create_dockerfile_and_compose.py` that creates:

     - A `Dockerfile` to containerize the FastAPI application.
     - A `docker-compose.yml` file to orchestrate the application and its dependencies.

     Ensure that the Docker configurations match the project's requirements and include necessary environment variables. The script should overwrite existing files and confirm upon completion.
     ```

10. **Master Script**

    - **Functional Prompt**:
      ```
      Generate a script named `setup_fountainai_ensemble.py` that executes all the previously generated Python scripts in the correct order to set up the FountainAI Ensemble Service project. The script should:

      - Execute each Python script and check for successful completion.
      - Provide a final confirmation message upon successful setup.
      ```

---

### Step 3: Execute Python Scripts Locally

**Objective**: Run the generated Python scripts to build or update your local project.

**Actions**:

- Save each Python script generated by GPT-4 with the appropriate filename.
- Execute the scripts in the correct order:
  ```sh
  python scripts/create_directory_structure.py
  python scripts/generate_schemas.py
  python scripts/generate_authentication.py
  python scripts/generate_models_and_crud.py
  python scripts/generate_typesense_sync.py
  python scripts/generate_logging.py
  python scripts/generate_api_routes.py
  python scripts/generate_main_entry.py
  python scripts/create_dockerfile_and_compose.py
  python scripts/setup_fountainai_ensemble.py
  ```

### Step 4: Validate FastAPI Implementation Against OpenAPI Specification

**Objective**: Ensure that the FastAPI application matches the OpenAPI specification exactly, not relying solely on automatic OpenAPI generation capabilities.

**Actions**:

- Verify that all endpoints include `operationId`, `summary`, and `description` in the route decorators to overwrite FastAPI's default behavior.
- Check that the Pydantic models, API routes, and other components match the OpenAPI specification in terms of field names, types, validations, and descriptions.
- Use FastAPI's `app.openapi_schema` to load the custom OpenAPI schema from `openapi3_1.yml`.
- Ensure that the generated FastAPI app explicitly defines the API according to the specification, rather than relying only on automatic generation.

### Step 5: Testing and Validation

**Objective**: Test the application to ensure it functions as expected and matches the OpenAPI specification.

**Actions**:

- Write test cases for each endpoint, validating that:
  - The endpoint paths, methods, parameters, and responses match the specification.
  - The authentication mechanisms work correctly.
  - Error handling behaves as defined.
- Use tools like `pytest` and `httpx` to automate testing.

---

## Next Steps

- **Initiate a GPT-4 session**, providing the functional prompts to generate the Python scripts.
- **Execute the Python scripts** in your local environment to set up the project.
- **Validate the FastAPI implementation** against the OpenAPI specification, ensuring that `operationId`, `summary`, and `description` are explicitly defined in the route decorators.
- **Write and run tests** to verify the application's functionality.
- **Use version control** to track changes and facilitate collaboration.

---

## License

This project is licensed under the terms of the MIT license.

---

## Appendix: Why Use a `main()` Function in Python Scripts?

Using a `main()` function is a common and recommended Python style for several reasons:

1. **Organization and Readability**:

   - Wrapping your code in a `main()` function makes it more organized and easier to read. It clearly separates the script's definition from its execution logic.

2. **Reusability**:

   - It allows the script to be reused as a module. If your script contains only standalone code, it will execute every time it's imported into another module. Using `main()` and `if __name__ == "__main__"` allows you to control when the script should execute.

3. **Scoping**:

   - Using a `main()` function helps keep the global scope clean, as any variables or logic within `main()` will not pollute the global namespace.

4. **Testability**:

   - It becomes easier to write unit tests for individual functions in the script. The `main()` function encapsulates the execution logic, allowing test scripts to focus on individual components rather than running the entire script.

### Common Usage Pattern

A typical Python script with a `main()` function looks like this:

```python
def main():
    # Your main logic here
    print("Running the main function.")

if __name__ == "__main__":
    main()
```

- **`main()`**** Function**: Defines the main logic of the script.
- **`if __name__ == "__main__"`**: This condition ensures that the `main()` function is only called when the script is run directly, not when it's imported.

This pattern is particularly common in **CLI tools**, **scripting**, and even in larger frameworks where clear delineation between script execution and function/module reusability is desired. Each script can run standalone or be managed by the master script without unintended execution.

---

Please feel free to contribute to this project by submitting issues or pull requests. If you have any questions or need further assistance, don't hesitate to reach out!

