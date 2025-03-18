from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from src.config import dev, prod
from fastapi.middleware.cors import CORSMiddleware
from routes import app as api_app

def create_app():
    config = dev.DevConfig()
    app = FastAPI(title=config.APP_NAME)
    # print(os.path.dirname(os.path.abspath(__file__)))


    # Add DBSessionMiddleware for managing database sessions
    app.add_middleware(DBSessionMiddleware, db_url=config.DATABASE_URL)

    # Include your routers
    app.include_router(api_app.router)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app = create_app()