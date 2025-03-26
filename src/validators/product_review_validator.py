from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator
from typing import List, Optional

class ReviewCreate(BaseModel):
    user_id: int
    product_id: int
    rating: float = Field(..., ge=1, le=5)
    review_text: Optional[str] = Field(None, max_length=1000)
    review_photo: Optional[List[HttpUrl]] = None  


    @field_validator("rating")
    @classmethod
    def validate_rating(cls, rate):
        if rate * 2 != int(rate * 2):
            raise ValueError("Rating must be in 0.5 increments (e.g., 3.5, 4.0)")
        return rate

    @field_validator("review_photo")
    @classmethod
    def validate_photo_url(cls, photo_urls):
        if photo_urls: 
            for photo_url in photo_urls:
                if not str(photo_url).lower().startswith(("http://", "https://")):
                    raise ValueError("Each URL in review_photo must be a valid URL")
        return photo_urls

    
    
    @field_validator("review_text")
    @classmethod
    def validate_review_text(cls, review_text):
        if review_text is not None:
            stripped = review_text.strip()
            if len(stripped) < 5:
                raise ValueError("review_text must be at least 5 characters")
            if not stripped:
                raise ValueError("review_text cannot be empty or only whitespace")
            
        return review_text


    @model_validator(mode="after")
    def validate_text_or_photo(self):
        if not self.review_text and not self.review_photo:
            raise ValueError("Either review_text or review_photo must be provided")
        return self
    
    
class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=1, le=5)
    review_text: Optional[str] = Field(None, max_length=1000)
    review_photo: Optional[List[HttpUrl]] = None  


    @field_validator("rating")
    @classmethod
    def validate_rating(cls, rating):
        if rating is not None and rating * 2 != int(rating * 2):
            raise ValueError("Rating must be in 0.5 increments (e.g., 4.0, 3.5)")
        return rating
    
    
    @field_validator("review_photo")
    @classmethod
    def validate_photo_url(cls, photo_urls):
        if photo_urls: 
            for photo_url in photo_urls:
                if not str(photo_url).lower().startswith(("http://", "https://")):
                    raise ValueError("Each URL in review_photo must be a valid URL")
        return photo_urls

    @model_validator(mode="after")
    def validate_text_or_photo(self):
        if (
            self.review_text is not None
            and self.review_text.strip() == ""
            and not self.review_photo
        ):
            raise ValueError("Either review_text or review_photo must be provided")
        return self
    
class ReviewReplyVal(BaseModel):
    user_id: int
    comment_text: str
    is_liked: bool
