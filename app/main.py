from fastapi import FastAPI
from app.handlers import auth_router


def get_app() -> FastAPI:
    appr = FastAPI(
        title='NoteMaster-API'
    )
    appr.include_router(auth_router)
    return appr


app = get_app()