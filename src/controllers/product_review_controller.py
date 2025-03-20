from fastapi import APIRouter

router = APIRouter()

from src.services.review_service import (
    get_product_reviews,
)

@router.get("/product-review/{product_review_id}")
async def get_product_reviews_all(product_review_id: int):
    return await get_product_reviews(product_review_id)