from functools import lru_cache

from fastapi import FastAPI, Depends
from typing_extensions import Annotated

from app.config import Settings
from app.handlers import auth_router


@lru_cache
def get_settings():
    return Settings()


def get_app(settings:  Annotated[Settings, Depends(get_settings)]) -> FastAPI:
    app = FastAPI(
        title=settings.app_name
    )
    app.include_router(auth_router)
    return app


app = get_app(get_settings())
