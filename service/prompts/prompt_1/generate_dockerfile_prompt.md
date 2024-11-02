Generate a script named `generate_dockerfile.py` that will be placed in `/service/scripts/`. This script should create a `Dockerfile`, `.dockerignore`, and `requirements.txt` in the appropriate locations within the repository.

1. **Dockerfile**:
   - Create a `Dockerfile` in the `/service` directory.
   - Use an official Python base image (e.g., `python:3.11-slim`).
   - Set the working directory to `/service`.
   - Install required system packages.
   - Copy the application code and `requirements.txt` into the container.
   - Install Python dependencies using `pip`.
   - Set environment variables as needed.
   - Specify the command to run the FastAPI application using Uvicorn.
   - Ensure idempotency by checking if the `Dockerfile` already exists before creating it.

2. **.dockerignore**:
   - Create a `.dockerignore` file in the root (`Ensemble-Service`) directory.
   - Include commonly ignored files and directories to improve Docker build efficiency.
   - Ensure idempotency by checking if the `.dockerignore` file already exists before creating it.

3. **requirements.txt**:
   - Create a `requirements.txt` file in the `/service` directory.
   - Include necessary dependencies like FastAPI, Uvicorn, Alembic, SQLAlchemy, and psycopg2.
   - Ensure idempotency by checking if the `requirements.txt` already exists before creating it.

4. **Idempotency and Error Handling**:
   - The script should be idempotent: it must check if each file already exists and skip creation if it does.
   - Implement comprehensive error handling to manage permission errors, missing directories, and general exceptions.

5. **Repository Structure**:
   - The script should adhere to the following structure:
     ```
     Ensemble-Service/
     ├── README.md
     ├── create_backup_and_prepare_next_iteration.sh
     ├── .dockerignore  # Created by the script
     └── service
         ├── README.md
         ├── Dockerfile  # Created by the script
         ├── requirements.txt  # Created by the script
         └── scripts
             └── generate_dockerfile.py  # The script you're writing
     ```
   - Ensure all paths are correctly defined to avoid redundant nesting or incorrect references.

Additionally, the `Dockerfile` should include the necessary tools for database migrations and a command to apply migrations (e.g., `alembic upgrade head`) as part of the container startup routine.


