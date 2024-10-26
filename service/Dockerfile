# Dockerfile for FountainAI Ensemble Service

# Use official Python base image
FROM python:3.11-slim

# Set working directory to /service
WORKDIR /service

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements.txt /service/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code to /service
COPY . /service

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port 8000
EXPOSE 8000

# Run the FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

