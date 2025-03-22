from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from src.models.base import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    profile_image = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now)

    review_replies = relationship('ReviewReply', back_populates='user', cascade='all, delete-orphan')
    # orders = db.relationship('Order', backref=db.backref('user', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'height': self.height,
            'weight': self.weight,
            'profile_image': self.profile_image,
            'created_at': self.created_at
        }