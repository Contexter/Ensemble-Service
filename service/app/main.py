
from fastapi import FastAPI, Request
from app.api.routes import root
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instantiate the FastAPI app
app = FastAPI()

# Include routers
app.include_router(root.router)

# Add middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response

# Event handlers
@app.on_event("startup")
async def startup_event():
    logger.info("Application is starting...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application is shutting down...")
