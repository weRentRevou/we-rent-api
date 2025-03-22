from fastapi import APIRouter
from src.schemas.product_schema import (
    ProductSchema,
    UpdateProductSchema
    
)

router = APIRouter()

from src.services.product_service import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product
)

@router.get("/products",tags=["Product Controller"])
async def get_all_products_controller():
    return await get_all_products()
@router.get("/product/{product_id}",tags=["Product Controller"])
async def get_product_by_id_controller(product_id: int):
    return await get_product_by_id(product_id)

@router.post("/product",tags=["Product Controller"])
async def create_product_controller(product_param: ProductSchema):
    return await create_product(product_param)

@router.put("/product/{product_id}",tags=["Product Controller"])
async def update_product_controller(product_id: int, product_param: UpdateProductSchema):
    return await update_product(product_id, product_param)

@router.delete("/product/{product_id}",tags=["Product Controller"])
async def delete_product_controller(product_id: int):
    return await delete_product(product_id)