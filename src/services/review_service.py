import math
from fastapi import Response
from fastapi.responses import JSONResponse
from typing import List, Optional
from sqlalchemy import asc, desc, func, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload
from app import db
from src.models.product_review_models import ProductReview
from src.models.user_models import User
from src.validators.product_review_validator import ReviewCreate, ReviewUpdate

async def get_product_reviews(
                product_id: int,
                rating: Optional[int] = None,
                has_photo: Optional[bool] = None,
                sort_by: Optional[str] = "newest",
                response: Optional[Response] = None

            ) -> JSONResponse:
    """Fetch all reviews for a given product, including aggregated rating and fit scale."""
    try:
        query = (
            db.session.query(ProductReview)
            .filter(ProductReview.product_id == product_id)
            .options(joinedload(ProductReview.replies), joinedload(ProductReview.user))
        )
        
        total_reviews = query.count()
        
        if rating is not None:
            query = query.filter(ProductReview.rating == rating)

        if has_photo is not None:
            if has_photo:
                query = query.filter(ProductReview.review_photo.isnot(None))
            else:
                query = query.filter(ProductReview.review_photo.is_(None))

        if sort_by == "newest":
            query = query.order_by(desc(ProductReview.created_at))
        elif sort_by == "oldest":
            query = query.order_by(asc(ProductReview.created_at))
            

        reviews = query.all()

        if not reviews:
            return JSONResponse(content={"error": "No reviews found for this product"}, status_code=404)

        avg_rating_query = db.session.execute(
            text("SELECT AVG(rating) FROM product_reviews WHERE product_id = :product_id"),
            {"product_id": product_id}
        )

        avg_rating = round(avg_rating_query.fetchone()[0] or 0, 1)

        fit_scale_counts = {
            "small": 0,
            "true_to_size": 0,
            "large": 0
        }

        for review in reviews:
            if review.rating <= 2.5:
                fit_scale_counts["small"] += 1
            elif review.rating >= 4.5:
                fit_scale_counts["large"] += 1
            else:
                fit_scale_counts["true_to_size"] += 1

        fit_scale_percentages = {
            key: round(count / len(reviews) * 100, 2) if len(reviews) > 0 else 0
            for key, count in fit_scale_counts.items()
        }

        review_list = []

        for review in reviews:
            review_data = review.to_dict()
            user = review.user
            user_details = {
                "id": user.id,
                "name": user.name,
                "height": user.height,
                "weight": user.weight,
                "body_size": user.body_size,
                "profile_image": user.profile_image or "link_to_default_image"
            }
            review_data["user"] = user_details
            review_data["likes"] = sum(1 for reply in review.replies if reply.is_liked)
            review_list.append(review_data)

        response_data = {
            "average_rating": avg_rating,
            "fit_scale": fit_scale_percentages,
            "reviews": review_list
        }

        if response is not None:
            response.headers["X-Total-Review"] = str(total_reviews)
            response.headers["X-Filtered-Review"] = str(len(reviews))
            
        return JSONResponse(content=response_data, status_code=200)

    except (IntegrityError, SQLAlchemyError) as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
    
    
async def create_product_review(review_data: ReviewCreate) -> JSONResponse:
    try:
        
        review_photo_strs = [str(photo) for photo in review_data.review_photo] if review_data.review_photo else []
        new_review = ProductReview(
            user_id=review_data.user_id,
            product_id=review_data.product_id,
            rating=math.floor(review_data.rating),
            review_text=review_data.review_text,
            review_photo=review_photo_strs  
        )

        db.session.add(new_review)
        db.session.commit()
        db.session.refresh(new_review)


        response_data = new_review.to_dict()
        
        return JSONResponse(status_code=201, content={"message": "Review created successfully", "data": response_data})

    except Exception as e:
        db.session.rollback()
        return JSONResponse(status_code=400, content={"message": f"An error occurred: {str(e)}"})


    
async def update_product_review(review_id: int, review_data: ReviewUpdate):
    try:
        review = db.session.query(ProductReview).filter_by(id=review_id).first()

        if not review:
            return JSONResponse(content={"error": "Review not found"}, status_code=404)
        
        review_photo_strs = [str(photo) for photo in review_data.review_photo] if review_data.review_photo else []
        print("Converted review_photo:", review_photo_strs)
        
        
        if review_data.rating is not None:
            review.rating = review_data.rating
        if review_data.review_text is not None:
            review.review_text = review_data.review_text
        if review_data.review_photo is not None:
            review.review_photo = review_photo_strs
            
        db.session.commit()
        db.session.refresh(review)

        return JSONResponse(
            content={
                "message": "Review updated successfully",
                "data": review.to_dict()
            },
            status_code=200
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
    


