from fastapi import APIRouter

from app.config import get_settings
from app.api_v1.endpoints.notes_category import note_category_router

notes_router = APIRouter(
        prefix=get_settings().urls.notes_prefix,
        tags=['notes'],
    )
notes_router.include_router(note_category_router)
