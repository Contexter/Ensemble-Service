# generate_docker_compose_prompt.md

Generate a script named `generate_docker_compose.py` that will be placed in `/service/scripts/`. This script should create a `docker-compose.yml` file in the `/service` root directory. The script should:

1. **Repository Verification**:
   - Verify if necessary files and directories exist in the repository, such as the Dockerfile and requirements.txt.

2. **docker-compose.yml**:
   - Create a `docker-compose.yml` in the `/service` directory with the following:
     - Defines services for the **FastAPI application** and **Typesense**.
     - Uses version `3.9` for the `docker-compose` file format.
     - **FastAPI service**:
       - Build the service using the `Dockerfile` present in `/service`.
       - Mounts the `/service` directory to allow code changes to be reflected without rebuilding the image.
       - Exposes port `8000` to the host.
       - Adds necessary environment variables for development.
       - Connects to a custom network named `fountain_network`.
     - **Typesense service**:
       - Uses the official **Typesense** image, version `0.24.0`.
       - Mounts a persistent volume named `typesense_data` to store data.
       - Exposes port `8108` to the host.
       - Uses the environment variable `TYPESENSE_API_KEY` for the Typesense configuration.
       - Connects to the same `fountain_network`.
     - **Network configuration**:
       - Defines a bridge network named `fountain_network`.
     - **Persistent volume**:
       - Creates a local volume named `typesense_data` to persist Typesense data across container restarts.

3. **Error Handling and Idempotency**:
   - Ensure idempotency by checking if the `docker-compose.yml` already exists before creating it.
   - Implement comprehensive error handling to manage permission errors, missing directories, and general exceptions.

4. **Repository Structure**:
   - The script should adhere to the following structure:
     ```
     Ensemble-Service/
     ├── README.md
     ├── create_backup_and_prepare_next_iteration.sh
     ├── .dockerignore
     └── service
         ├── Dockerfile
         ├── README.md
         ├── docker-compose.yml  # Created by the script
         ├── requirements.txt
         └── scripts
             └── generate_docker_compose.py  # The script you're writing
     ```
   - Ensure all paths are correctly defined to avoid redundant nesting or incorrect references.

5. **Execution Notes**:
   - The Dockerfile should be located in the `/service` directory and include instructions to set up the FastAPI app.
   - The script should be run from the `/service/scripts/` directory.
   - The generated `docker-compose.yml` should reference correct relative paths to avoid recursive issues.
   - Verify repository state before creating the `docker-compose.yml` file to avoid runtime errors.
   - Use a secure method to handle the Typesense API key, such as environment variables.

The script should ensure that the Docker services for **FastAPI** and **Typesense** are configured properly, taking into account persistent data storage, development convenience, and reusable configurations.

