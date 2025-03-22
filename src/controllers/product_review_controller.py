from typing import Literal, Optional
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse

from src.validators.product_review_validator import ReviewCreate, ReviewUpdate

router = APIRouter()

from src.services.review_service import (
    get_product_reviews,
    create_product_review,
    update_product_review
)

@router.get("/product-review/{product_review_id}", tags=["Product Review"])
async def get_product_reviews_all(product_review_id: int,
    rating: Optional[int] = None,
    has_photo: Optional[bool] = None,
    sort_by: Optional[Literal["newest", "oldest"]] = "newest",
    response: Response = None):
    
    if rating is not None and (rating < 1 or rating > 5):
        return JSONResponse(content={"error": "Rating must be between 1 and 5"}, status_code=400)
        
    return await get_product_reviews(
        product_id=product_review_id,
        rating=rating,
        has_photo=has_photo,
        sort_by=sort_by,
        response=response
    )
    
@router.post("/product-review", tags=["Product Review"],
             description="Create a new product review. Requires user ID, rating, and at least one of review_text or review_photo.")
async def create_product_review_controller(review: ReviewCreate):
    return await create_product_review(review)


@router.put("/product-review/{review_id}", tags=["Product Review"])
async def update_product_review_controller(review_id: int, review: ReviewUpdate):
    return await update_product_review(review_id, review)