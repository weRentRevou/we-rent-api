from fastapi import APIRouter

router = APIRouter()

@router.get("/review-reply/{review_reply_id}")
async def get_review_reply(review_reply_id: int):
    return await {"review_reply_id": review_reply_id}