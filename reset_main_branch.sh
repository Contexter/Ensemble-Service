#!/bin/bash

# Script Name: reset_main_branch.sh

# Exit immediately if a command exits with a non-zero status
set -e

# Variables
REPO_URL="https://github.com/Contexter/Ensemble-Service.git"
BACKUP_BRANCH="backup-main-$(date +%Y%m%d%H%M%S)"
NEW_MAIN_BRANCH="main"

# Function to create a backup branch
create_backup_branch() {
  git fetch origin
  git checkout -b $BACKUP_BRANCH origin/main
  git push origin $BACKUP_BRANCH
}

# Function to delete the existing main branch locally
delete_local_main_branch() {
  git branch -D $NEW_MAIN_BRANCH || true
}

# Function to create a new main branch from scratch
create_new_main_branch() {
  git checkout --orphan $NEW_MAIN_BRANCH
  git rm -rf .
  git commit --allow-empty -m "Drop Kong in favor of a pure FastAPI app acting as FountainAI service mediator"
  git push -f origin $NEW_MAIN_BRANCH
}

# Main script execution
create_backup_branch
delete_local_main_branch
create_new_main_branch

# Clean up
echo "Backup branch '$BACKUP_BRANCH' created and new main branch initialized."
