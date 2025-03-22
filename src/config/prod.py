from .base import BaseConfig
from typing import ClassVar, List
import os
from dotenv import load_dotenv

load_dotenv(override=True)

class ProdConfig(BaseConfig):
    DATABASE_URL: str = os.getenv("DB_URI_PROD")
    # JWT_SECRET: str = os.getenv("JWT_SECRET")
    # Use ClassVar to indicate these are not Pydantic model fields
    ALGORITHM: ClassVar[str] = "HS512"
    ACCESS_TOKEN_EXPIRE_MINUTES: ClassVar[int] = 30
    # SECRET_KEY: str = os.getenv("KEY_SECRET")

    # Define allowed origins
    origins: ClassVar[List[str]] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
