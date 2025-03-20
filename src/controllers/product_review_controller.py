from fastapi import APIRouter

router = APIRouter()

@router.get("/product-review/{product_review_id}")
async def get_product_review(product_review_id: int):
    return await {"product_review_id": product_review_id}