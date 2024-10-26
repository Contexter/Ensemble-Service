
from fastapi import APIRouter

router = APIRouter()

@router.get("/root")
def root_endpoint():
    return {"message": "This is the root endpoint."}
