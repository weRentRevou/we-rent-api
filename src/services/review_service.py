from fastapi.responses import JSONResponse
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload
from app import db
from src.models.product_review_models import ProductReview
from src.models.user_models import User
from src.models.review_reply import ReviewReply

async def get_product_reviews(product_id: int) -> JSONResponse:
    """Fetch all reviews for a given product, including aggregated rating and fit scale."""
    try:
        reviews = (
            db.session.query(ProductReview)
            .filter(ProductReview.product_id == product_id)
            .options(joinedload(ProductReview.replies), joinedload(ProductReview.user))
            .all()
        )

        if not reviews:
            return JSONResponse(content={"error": "No reviews found for this product"}, status_code=404)

        
        #might change it later to find avg rating of all reviews
        avg_rating_query = db.session.execute(
            "SELECT AVG(rating) FROM product_reviews WHERE product_id = :product_id",
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

        return JSONResponse(content=response_data, status_code=200)

    except (IntegrityError, SQLAlchemyError) as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

