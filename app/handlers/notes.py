from fastapi import APIRouter

from app.config import get_settings

notes_router = APIRouter(
        prefix=get_settings().urls.notes_prefix,
        tags=['notes'],
    )
