from fastapi import FastAPI, Depends, APIRouter
from typing_extensions import Annotated

from app.config import Settings, get_settings
from app.api_v1.endpoints import base, notes, users, notes_category


def get_app(settings: Annotated[Settings, Depends(get_settings)]) -> FastAPI:
    app = FastAPI(
        title=settings.app_name
    )
    v1 = APIRouter(
        prefix=settings.urls.api_version_prefix,
        # tags=['v1'],
    )

    group_notes_router = APIRouter(
        prefix=get_settings().urls.notes_prefix,
        tags=['notes'],
        dependencies=[Depends(users.oauth_scheme)]  # lock all /notes endpoints
    )
    group_notes_router.include_router(notes.notes_router)
    group_notes_router.include_router(notes_category.note_category_router)

    v1.include_router(base.base_router)
    v1.include_router(users.users_router)
    v1.include_router(group_notes_router)

    app.include_router(v1)

    return app


app = get_app(get_settings())
