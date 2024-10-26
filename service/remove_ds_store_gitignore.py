import os
import subprocess
import logging

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

# Configure logging
logging.basicConfig(filename='ds_store_cleanup.log', level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

def remove_ds_store_files():
    """
    Remove all .DS_Store files from the repository.
    """
    for root, dirs, files in os.walk(REPO_ROOT, topdown=True):
        depth = root[len(REPO_ROOT):].count(os.sep)
        if depth > 2:  # Limit depth to improve performance for large repositories
            continue
        for file in files:
            if file == '.DS_Store':
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Removed: {file_path}")
                except PermissionError:
                    logging.warning(f"Permission denied while removing {file_path}")
                except FileNotFoundError as e:
                    print(f"File not found while removing {file_path}: {e}")
                except OSError as e:
                    print(f"OS error while removing {file_path}: {e}")

def ensure_ds_store_in_gitignore():
    """
    Ensure that .DS_Store is in the .gitignore file.
    """
    gitignore_path = os.path.join(REPO_ROOT, '.gitignore')
    ds_store_entry = '.DS_Store'

    try:
        if not os.path.exists(gitignore_path):
            # Create a .gitignore file if it doesn't exist
            with open(gitignore_path, 'w') as gitignore:
                gitignore.write(ds_store_entry + '\n')
            print(f"Created .gitignore and added {ds_store_entry}")
        else:
            # Check if .DS_Store is already in the .gitignore
            with open(gitignore_path, 'r') as gitignore:
                lines = set(line.strip() for line in gitignore)

            if ds_store_entry not in lines:
                # Add .DS_Store to the .gitignore if it's not present
                with open(gitignore_path, 'a') as gitignore:
                    gitignore.write(ds_store_entry + '\n')
                print(f"Added {ds_store_entry} to .gitignore")
            else:
                print(f"{ds_store_entry} is already in .gitignore")
    except IOError as e:
        print(f"Error handling .gitignore file: {e}")

def main():
    remove_ds_store_files()
    ensure_ds_store_in_gitignore()

    # Verify .DS_Store has been removed from git
    try:
        result = subprocess.run(["git", "rm", "--cached", "-r", "--ignore-unmatch", "*.DS_Store"], check=True, capture_output=True, text=True)
        print("Verified: Removed .DS_Store files from Git index.")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error removing .DS_Store from Git index: {e.stderr}")
    except subprocess.SubprocessError as e:
        logging.error(f"A subprocess error occurred while removing .DS_Store from Git index: {e}")
        print(f"A subprocess error occurred: {e}")

if __name__ == "__main__":
    main()

