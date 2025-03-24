from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app import db
from src.models.user_models import User

from src.schemas.user_schema import (
    UserSchema,
    UpdateUserSchema
)

async def get_all_users():
    try:
        users = db.session.query(User).all()
        return JSONResponse(content=[{
                "data": user_data.to_dict()
            }   for user_data in users
                                     
            ], 
            status_code=200,
        )
    except SQLAlchemyError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

async def get_user_by_id(user_id: int):
    try:
        user = db.session.query(User).get(user_id)
        if user:
            return JSONResponse(content={"data": user.to_dict()}, status_code=200)
        else:
            return JSONResponse(content={"error": "User not found"}, status_code=404)
    except SQLAlchemyError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
async def create_user(user_param: UserSchema):
    try:
        existing_user = db.session.query(User).filter_by(name=user_param.name).first()
        if existing_user:
            return JSONResponse(content={"error": "User already exists"}, status_code=400)
        user = User(
            # id=user_param.user_id,
            body_size=user_param.body_size if user_param.body_size else None,
            name=user_param.name,
            height=user_param.height,
            weight=user_param.weight,
            profile_image=user_param.profile_image
        )
        db.session.add(user)
        db.session.commit()
        return JSONResponse(content={"message": "User created successfully",
                                     "data": user.to_dict()}, status_code=201)
    except SQLAlchemyError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
async def update_user(user_id: int, user_param: UpdateUserSchema):
    try:
        user = db.session.query(User).get(user_id)
        if not user:
            return JSONResponse(content={"error": "User not found"}, status_code=404)

        # Only update fields that were actually passed in the request
        update_data = user_param.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        db.session.commit()

        return JSONResponse(
            content={
                "message": "User updated successfully",
                "data": user.to_dict()
            },
            status_code=200
        )

    except SQLAlchemyError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
async def delete_user(user_id: int):
    try:
        user = db.session.query(User).get(user_id)
        if not user:
            return JSONResponse(content={"error": "User not found"}, status_code=404)

        db.session.delete(user)
        db.session.commit()

        return JSONResponse(content={"message": "User deleted successfully"}, status_code=200)

    except SQLAlchemyError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)