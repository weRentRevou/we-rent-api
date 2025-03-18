from fastapi import APIRouter
from src.services.test_service import test_access

router = APIRouter()

@router.get("/")
def hello():
    return {"message": "FastAPI We Rent Project"}