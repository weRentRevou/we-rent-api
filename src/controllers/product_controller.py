from fastapi import APIRouter

router = APIRouter()

from src.services.product_service import (
    get_all_products
)

@router.get("/products")
async def get_all_products_controller():
    return await get_all_products()
@router.get("/product/{product_id}")
async def get_product(product_id: int):
    return await {"product_id": product_id}