from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app import db
from src.models.product_models import Product
from src.schemas.product_schema import (
    ProductSchema,
    UpdateProductSchema
)
async def get_all_products():
    try:
        products = db.session.query(Product).all()
        return JSONResponse(content=[{
                "data": product_data.to_dict()
            }   for product_data in products
                                     
            ], 
            status_code=200,
            # headers={"X-Custom-Header": "Hello from FastAPI"}
        )
    except SQLAlchemyError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
async def get_product_by_id(product_id: int):
    try:
        product = db.session.query(Product).get(product_id)
        if product:
            return JSONResponse(content={"data": product.to_dict()}, status_code=200)
        else:
            return JSONResponse(content={"error": "Product not found"}, status_code=404)
    except SQLAlchemyError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
async def create_product(product_param: ProductSchema):
    try:
        product = Product(
            user_id=product_param.user_id if product_param.user_id else None,
            name=product_param.name,
            description=product_param.description,
            price=product_param.price,
            size=product_param.size,
            bust=product_param.bust,
            length=product_param.length,
            fabric=product_param.fabric,
            fit=product_param.fit,
            product_image=product_param.product_image,
            designer_photo=product_param.designer_photo
        )
        db.session.add(product)
        db.session.commit()
        return JSONResponse(content={"message": "Product created successfully",
                                     "data": product.to_dict()}, status_code=201)
    except SQLAlchemyError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

async def update_product(product_id: int, product_param: UpdateProductSchema):
    try:
        product = db.session.query(Product).get(product_id)
        if not product:
            return JSONResponse(content={"error": "Product not found"}, status_code=404)

        # Only update fields that were actually passed in the request
        update_data = product_param.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)

        db.session.commit()

        return JSONResponse(
            content={
                "message": "Product updated successfully",
                "data": product.to_dict()
            },
            status_code=200
        )

    except SQLAlchemyError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
async def delete_product(product_id: int):
    try:
        product = db.session.query(Product).get(product_id)
        if not product:
            return JSONResponse(content={"error": "Product not found"}, status_code=404)

        db.session.delete(product)
        db.session.commit()

        return JSONResponse(content={"message": "Product deleted successfully"}, status_code=200)

    except SQLAlchemyError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)