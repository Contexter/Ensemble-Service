import os
from concurrent.futures import ThreadPoolExecutor

def create_directory(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created directory: {path}")
        else:
            print(f"Directory already exists: {path}")
    except OSError as e:
        print(f"Error creating directory {path}: {e}")

def create_file(path, content=""):
    try:
        if not os.path.exists(path):
            with open(path, "w") as file:
                file.write(content)
            print(f"Created file: {path}")
        else:
            print(f"File already exists: {path}")
    except (OSError, IOError) as e:
        print(f"Error creating file {path}: {e}")

def main():
    # Define base directory
    base_dir = os.getenv("BASE_DIR", "/service/app")

    # Directories to be created
    directories = [
        f"{base_dir}/",
        f"{base_dir}/api/routes/",
        f"{base_dir}/models/",
        f"{base_dir}/schemas/",
        f"{base_dir}/crud/",
        f"{base_dir}/core/",
        f"{base_dir}/auth/",
        f"{base_dir}/typesense/",
        f"{base_dir}/tests/"
    ]

    # Create directories without redundant checks
    directories_to_create = [d for d in directories if not os.path.exists(d)]
    for directory in directories_to_create:
        create_directory(directory)

    # Initial files to be created
    files = {
        f"{base_dir}/main.py": """
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FountainAI Ensemble Service"}
""",
        f"{base_dir}/api/routes/__init__.py": "",
        f"{base_dir}/api/routes/root.py": """
from fastapi import APIRouter

router = APIRouter()

@router.get("/root")
def root_endpoint():
    return {"message": "This is the root endpoint."}
"""
    }

    # Create __init__.py files in each package as needed
    init_files = [
        f"{base_dir}/api/__init__.py",
        f"{base_dir}/models/__init__.py",
        f"{base_dir}/schemas/__init__.py",
        f"{base_dir}/crud/__init__.py",
        f"{base_dir}/core/__init__.py",
        f"{base_dir}/auth/__init__.py",
        f"{base_dir}/typesense/__init__.py",
        f"{base_dir}/tests/__init__.py"
    ]

    init_files_to_create = [f for f in init_files if not os.path.exists(f)]

    # Create all files in parallel to improve performance
    with ThreadPoolExecutor() as executor:
        executor.map(create_file, init_files_to_create)
        executor.map(lambda item: create_file(*item), files.items())

if __name__ == "__main__":
    main()

