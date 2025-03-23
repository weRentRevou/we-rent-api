from pydantic import BaseModel
from typing import Optional

class ProductSchema(BaseModel):
    name: str
    description: str
    price: float
    size: Optional[str] = None
    bust: Optional[float] = None
    length: Optional[float] = None
    fabric: Optional[str] = None
    fit: Optional[str] = None
    product_image: Optional[str] = None

    class Config:
        from_attributes = True


class UpdateProductSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    size: Optional[str] = None
    bust: Optional[float] = None
    length: Optional[float] = None
    fabric: Optional[str] = None
    fit: Optional[str] = None
    product_image: Optional[str] = None

    class Config:
        from_attributes = True