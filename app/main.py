from fastapi import FastAPI, Depends, APIRouter
from typing_extensions import Annotated

from app.config import Settings, get_settings
from app.handlers import users, notes, base


def get_app(settings: Annotated[Settings, Depends(get_settings)]) -> FastAPI:
    app = FastAPI(
        title=settings.app_name
    )
    v1 = APIRouter(
        prefix='/v1',
        # tags=['v1'],
    )
    v1.include_router(base.base_router)
    v1.include_router(users.users_router)
    v1.include_router(notes.notes_router)

    app.include_router(v1)

    return app


app = get_app(get_settings())
