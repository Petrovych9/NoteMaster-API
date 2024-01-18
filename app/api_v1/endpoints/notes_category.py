from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter, status

from app.domain import note_categories_models as m
from app.domain.note_categories_crud import get_notes_categories_crud, NoteCategoryCrud
from app.domain.error_models import ErrorResponse
from app.domain.validation import Validator, get_validator
from app.config import get_settings, Settings


note_category_router = APIRouter(
    prefix=get_settings().urls.note_category_prefix,
    )


@note_category_router.post(get_settings().urls.notes_category.create, name='category: create')
async def create_category(
        data: m.CreateNoteCategoryRequest,
        note_category_db: NoteCategoryCrud = Depends(get_notes_categories_crud),
        settings: Settings = Depends(get_settings),
        validator: Validator = Depends(Validator),
):
    return m.CreatedNoteCategoryResponse()


@note_category_router.post(get_settings().urls.notes_category.update, name='category: update')
async def update_category(
        data: m.UpdateCategoryRequest,
        note_category_db: NoteCategoryCrud = Depends(get_notes_categories_crud),
        settings: Settings = Depends(get_settings),
        validator: Validator = Depends(Validator),
):
    return m.UpdateCategoryResponse()


@note_category_router.post(get_settings().urls.notes_category.delete, name='category: delete')
async def delete_category(
        data: m.DeleteCategoryRequest,
        note_category_db: NoteCategoryCrud = Depends(get_notes_categories_crud),
        settings: Settings = Depends(get_settings),
        validator: Validator = Depends(Validator),
):
    return m.DeleteCategoryResponse()
