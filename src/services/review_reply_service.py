import json
from fastapi.responses import JSONResponse
from app import db
from sqlalchemy.future import select
from src.models.review_reply import ReviewReply
from src.validators.product_review_validator import ReviewReplyVal
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

async def create_reply_review(review_id: int, reply_data: ReviewReplyVal):
    try:
        new_reply = ReviewReply(
            review_id=review_id,
            user_id=reply_data.user_id,
            comment_text=reply_data.comment_text,
            is_liked=reply_data.is_liked
        )
        
        db.session.add(new_reply)
        db.session.commit()
        db.session.refresh(new_reply)
        
        return JSONResponse(
            content={
                "message": "Review reply created successfully",
                "data": new_reply.to_dict()
            },
            status_code=201
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
async def get_replies_review(review_id: int):
    try:
        replies = (db.session.query(ReviewReply).where(ReviewReply.review_id == review_id).all())
            
        if not replies:
            return {"error": "Reply not found"}
        
        return JSONResponse(
            content={
                "message": "Get review replies {review_id} id successfully",
                "data": [reply.to_dict() for reply in replies]
            },
            status_code=200
        )
    except (IntegrityError, SQLAlchemyError) as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)