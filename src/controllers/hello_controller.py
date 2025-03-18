from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def hello():
    return {"message": "FastAPI We Rent Project"}