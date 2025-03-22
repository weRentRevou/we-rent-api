from fastapi import APIRouter

from src.services.review_reply_service import create_reply_review, get_replies_review
from src.validators.product_review_validator import ReviewReplyVal

router = APIRouter()

@router.get("/review-reply/{review_id}", tags=["Product Review"])
async def get_review_replies(review_id: int):
    return await get_replies_review(review_id=review_id)

@router.post("/review-reply/{review_id}", tags=["Product Review"])
async def create_review_reply(review_id: int, reply_data: ReviewReplyVal):
    return await create_reply_review(review_id, reply_data)