#!/bin/bash

# Function to initialize paths
initialize_paths() {
    BASE_DIR=$(dirname $(realpath $0))
    SERVICE_DIR="$BASE_DIR/service"
    PROMPTS_DIR="$SERVICE_DIR/prompts"
}

# Function to get the number of prompts as per the development plan
get_number_of_prompts_from_plan() {
    # Set the number of prompts manually based on the development plan
    NUM_PROMPTS=18  # Replace this number with the actual number from the plan
}

# Function to create the prompts directory if it doesn't exist
create_prompts_directory() {
    if [ ! -d "$PROMPTS_DIR" ]; then
        mkdir "$PROMPTS_DIR"
        echo "Created prompts directory at $PROMPTS_DIR"
    else
        echo "Prompts directory already exists at $PROMPTS_DIR"
    fi
}

# Function to create numbered prompt directories within the prompts directory
create_numbered_prompt_directories() {
    for ((i=1; i<=NUM_PROMPTS; i++))
    do
        PROMPT_SUBDIR="$PROMPTS_DIR/prompt_$i"
        if [ ! -d "$PROMPT_SUBDIR" ]; then
            mkdir "$PROMPT_SUBDIR"
            echo "Created prompt directory: $PROMPT_SUBDIR"
        else
            echo "Prompt directory already exists: $PROMPT_SUBDIR"
        fi
    done
}

# Main function to orchestrate the script execution
main() {
    initialize_paths
    get_number_of_prompts_from_plan
    create_prompts_directory
    create_numbered_prompt_directories
    echo "Prompts directory setup complete. Total prompt directories: $NUM_PROMPTS"
}

# Execute the main function
main

