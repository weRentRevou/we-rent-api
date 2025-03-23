from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    # user_id: Optional[int]
    name: str
    height: float
    weight: float
    profile_image: Optional[str] = None

    class Config:
        from_attributes = True

class UpdateUserSchema(BaseModel):
    name: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    profile_image: Optional[str] = None

    class Config:
        from_attributes = True