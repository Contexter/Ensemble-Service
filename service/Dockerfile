# Use an official Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /service

# Install required system packages
RUN apt-get update
RUN apt-get install -y build-essential libpq-dev     && rm -rf /var/lib/apt/lists/*

# Copy application code and scripts into the container
COPY ./service/ /service/
COPY ./service/requirements.txt /service/requirements.txt

# Create and activate a virtual environment
RUN python -m venv /service/venv
ENV PATH="/service/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --no-cache-dir -r /service/requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set CMD to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]