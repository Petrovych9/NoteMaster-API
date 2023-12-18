from fastapi import FastAPI
from app.handlers import auth_router


def get_app() -> FastAPI:
    app = FastAPI(
        title='NoteMaster-API'
    )
    app.include_router(auth_router)
    return app


app = get_app()
