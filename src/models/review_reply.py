from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from src.models.base import Base
from datetime import datetime

class ReviewReply(Base):
    __tablename__ = 'review_replies'

    id = Column(Integer, primary_key=True)
    review_id = Column(Integer, ForeignKey('product_reviews.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    comment_text = Column(Text, nullable=True)
    is_liked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now)

    review = relationship('ProductReview', back_populates="replies")
    user = relationship('User', back_populates="review_replies")

    def to_dict(self):
        return {
            'id': self.id,
            'review_id': self.review_id,
            "user": {
                "id": self.user.id,
                "username": self.user.name,
                "email": self.user.profile_image
            },
            'comment_text': self.comment_text,
            'is_liked': self.is_liked,
            'created_at': self.created_at.isoformat() if self.created_at else None,  # Avoid NoneType error
            'updated_at': self.updated_at.isoformat() if self.updated_at else None  # Handle updated_at as well
        }