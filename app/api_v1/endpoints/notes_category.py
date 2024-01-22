from fastapi import Depends, HTTPException, APIRouter, status

from app.domain.notes_category import note_categories_models as m
from app.domain.notes_category.note_categories_crud import get_notes_categories_crud, NoteCategoryCrud
from app.domain.error_models import ErrorResponse
from app.domain.validation import Validator
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
    # check if exist
    note_category = note_category_db.get_by_name(
        category_name=data.name
    )
    if note_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exist"
        )

    note_category_id = note_category_db.create(data)
    if not note_category_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.CREATING_NOTE_CATEGORY_ERROR

        )
    return m.CreatedNoteCategoryResponse()


@note_category_router.post(get_settings().urls.notes_category.update, name='category: update')
async def update_category(
        data: m.UpdateCategoryRequest,
        note_category_db: NoteCategoryCrud = Depends(get_notes_categories_crud),
        settings: Settings = Depends(get_settings),
        validator: Validator = Depends(Validator),
):

    if not (data.new_name or data.new_description):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Nothing to update'
        )

    # check if category exist
    note_category = note_category_db.get_by_name(
        category_name=data.category_name
    )
    if not note_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong category name"
        )

    update_fields = {}
    if data.new_name:
        update_fields['name'] = data.new_name
    if data.new_description:
        update_fields['description'] = data.new_description

    updated_note_category_id = note_category_db.update(
        category_id=note_category.id,
        field_value=update_fields
    )
    if not updated_note_category_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.UPDATING_NOTE_CATEGORY_ERROR
        )

    return m.UpdateCategoryResponse()


@note_category_router.post(get_settings().urls.notes_category.delete, name='category: delete')
async def delete_category(
        data: m.DeleteCategoryRequest,
        note_category_db: NoteCategoryCrud = Depends(get_notes_categories_crud),
        settings: Settings = Depends(get_settings),
        validator: Validator = Depends(Validator),
):
    note_category = note_category_db.get_by_name(
        category_name=data.category
    )
    if not note_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong category name"
        )

    del_messege = note_category_db.delete(note_category.id)
    if not del_messege:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.DELETING_NOTE_CATEGORY_ERROR
        )
    return m.DeleteCategoryResponse()
