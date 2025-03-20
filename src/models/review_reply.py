from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from src.models.base import Base
from datetime import datetime

class ReviewReply(Base):
    __tablename__ = 'review_replies'

    id = Column(Integer, primary_key=True)
    review_id = Column(Integer, ForeignKey('product_reviews.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    comment_text = Column(Text, nullable=False)
    is_liked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now)

    review = relationship('ProductReview', back_populates="replies")

    def to_dict(self):
        return {
            'id': self.id,
            'review_id': self.review_id,
            'user_id': self.user_id,
            'comment_text': self.comment_text,
            'is_liked': self.is_liked,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }