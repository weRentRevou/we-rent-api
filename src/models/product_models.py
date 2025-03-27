from sqlalchemy import Column, Integer, String, DateTime, Float, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base
from datetime import datetime

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(16, 2), nullable=False)
    size = Column(String(50), nullable=True)
    bust = Column(Float, nullable=True)
    length = Column(Float, nullable=True)
    fabric = Column(String(100), nullable=True)
    fit = Column(String(100), nullable=True)
    product_image = Column(String(255), nullable=True)
    designer_photo = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now)

    reviews = relationship('ProductReview', back_populates="product")
    # orders = relationship('Order', backref=db.backref('product', lazy=True))
    users = relationship('User', back_populates="products")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id if self.user_id is not None else None,
            'description': self.description,
            'price': float(self.price) if self.price is not None else None,  # Convert Decimal to float safely
            'size': self.size,
            'bust': self.bust,
            'length': self.length,
            'fabric': self.fabric,
            'fit': self.fit,
            'product_image': self.product_image,
            'designer_photo': self.designer_photo,
            'created_at': self.created_at.isoformat() if self.created_at else None,  # Avoid NoneType error
            'updated_at': self.updated_at.isoformat() if self.updated_at else None  # Handle updated_at as well
        }