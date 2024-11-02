#!/bin/bash

# Function to check if GitHub CLI is installed
check_gh_cli() {
  gh --version > /dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo "GitHub CLI (gh) is not installed. Please install it to use this script."
    exit 1
  fi
}

# Function to check if the repository is clean
check_repo_clean() {
  if [ -n "$(git status --porcelain)" ]; then
    echo "Your working directory is not clean. Please commit or stash changes before running the script."
    exit 1
  fi
}

# Function to get the current branch name
get_current_branch() {
  current_branch=$(git branch --show-current)
  if [ -z "$current_branch" ]; then
    echo "Could not determine the current branch. Make sure you are on a branch."
    exit 1
  fi
}

# Function to determine the iteration number for the backup branch
determine_iteration_number() {
  iteration=1
  while gh repo view >/dev/null 2>&1 && git rev-parse --verify "iteration-$iteration" >/dev/null 2>&1; do
    iteration=$((iteration + 1))
  done
}

# Function to create the backup branch using GitHub CLI
create_backup_branch() {
  gh repo clone $(gh repo view --json name -q '.name') tmp_repo
  cd tmp_repo || exit 1
  git checkout -b "iteration-$iteration"
  git push -u origin "iteration-$iteration"
  cd ..
  rm -rf tmp_repo
}

# Function to remove files and directories, except for specific files
clean_repository() {
  find . -maxdepth 1 ! -name 'README.md' ! -name '.gitignore' ! -name '.' ! -name '..' ! -name '.git' ! -name 'create_backup_and_prepare_next_iteration.sh' -exec rm -rf {} +
}

# Function to create the service directory and README
create_service_directory() {
  mkdir -p service
  echo -e "# Iteration $((iteration + 1))\n\nThis iteration starts with a clean and optimized repository." > service/README.md
}

# Function to commit the changes for the next iteration
commit_next_iteration() {
  git add .
  git commit -m "Prepare repository for iteration $((iteration + 1))"
}

# Function to prepare the repository for the next iteration
prepare_next_iteration() {
  clean_repository
  create_service_directory
  commit_next_iteration
}

# Main script execution
check_gh_cli
check_repo_clean
get_current_branch
determine_iteration_number
create_backup_branch
prepare_next_iteration

echo "Backup branch 'iteration-$iteration' created and repository prepared for iteration $((iteration + 1))."
