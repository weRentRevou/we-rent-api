from fastapi import APIRouter
from src.schemas.user_schema import (
    UserSchema,
    UpdateUserSchema
)

router = APIRouter()

from src.services.user_service import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user
)
@router.get("/users", tags=["User Controller"])
async def get_all_users_controller():
    return await get_all_users()

@router.get("/user/{user_id}", tags=["User Controller"])
async def get_user_by_id_controller(user_id: int):
    return await get_user_by_id(user_id)

@router.post("/users", tags=["User Controller"])
async def create_user_controller(user_param: UserSchema):
    return await create_user(user_param)

@router.put("/user/{user_id}", tags=["User Controller"])
async def update_user_controller(user_id: int, user_param: UpdateUserSchema):
    return await update_user(user_id, user_param)

@router.delete("/user/{user_id}", tags=["User Controller"])
async def delete_user_controller(user_id: int):
    return await delete_user(user_id)