from sqlalchemy import ARRAY, Column, Integer, String, DateTime, Float, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base
from datetime import datetime

class ProductReview(Base):
    __tablename__ = 'product_reviews'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    review_text = Column(Text, nullable=True)
    rating = Column(Float, nullable=False)
    review_photo =  Column(ARRAY(String(2048)), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now)

    product = relationship('Product', back_populates="reviews")
    replies = relationship('ReviewReply', back_populates="review")
    user = relationship('User')  
    
    def to_dict(self):
        converted_photo = self.review_photo
        if isinstance(converted_photo, list) and all(isinstance(c, str) and len(c) == 1 for c in converted_photo):
            joined_str = "".join(converted_photo).strip("{}")
            converted_photo = [url.strip() for url in joined_str.split(",") if url.strip()]

        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'review_text': self.review_text,
            'rating': self.rating,
            'review_photo': converted_photo or [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }