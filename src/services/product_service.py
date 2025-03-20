from fastapi.responses import JSONResponse
from typing import List, Optional
# from sqlalchemy.orm import aliased
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app import db
from src.models.product_models import Product

async def get_all_products():
    try:
        products = db.session.query(Product).all()
        return JSONResponse(content=[{
                "data": product_data.to_dict()
            }   for product_data in products
                                     
            ], status_code=200
        )
    except SQLAlchemyError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
