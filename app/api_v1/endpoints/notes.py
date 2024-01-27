from fastapi import APIRouter, Depends, HTTPException, status

from app.api_v1.endpoints.users import oauth_scheme
from app.config import get_settings, Settings
from app.domain.notes import note_models as m
from app.domain.notes.notes_crud import NotesCrud, get_notes_crud

from app.domain.notes_category.note_categories_crud import NoteCategoryCrud, get_notes_categories_crud

from app.domain.validation import Validator, get_validator
from app.domain.error_models import ErrorResponse

from app.domain.helper import Helper, get_helper

notes_router = APIRouter()


@notes_router.post(get_settings().urls.notes_endpoints.create, name='note: create')
async def create_note(
        data: m.CreateNoteRequest,
        note_db: NotesCrud = Depends(get_notes_crud),
        settings: Settings = Depends(get_settings),
        validator: Validator = Depends(Validator),
        helper: Helper = Depends(get_helper),
        token: str = Depends(oauth_scheme),
):
    if not data.title and not data.content:
        return m.CreatedNoteResponse(message='Nothing to create')

    fields = {}
    user = helper.get_current_user(token)
    fields.update(user_id=user.id)
    if data.title:
        fields.update(title=data.title)
    if data.content:
        fields.update(content=data.content)

    if data.category is not None:
        category_id = helper.get_category_id_by_name_or_create_new(
            category_name=data.category
        )
        if not category_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ErrorResponse.CREATING_NOTE_ERROR
            )
        fields.update(category_id=category_id)

    data = m.CreateNoteDbModel(**fields)
    note_id = note_db.create(note_model=data)
    print('created note id:', note_id)
    if not note_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.CREATING_NOTE_ERROR

        )
    return m.CreatedNoteResponse()


@notes_router.post(get_settings().urls.notes_endpoints.update, name='note: update')
async def update_note(
        data: m.UpdateNoteRequest,
        note_db: NotesCrud = Depends(get_notes_crud),
        note_category_db: NoteCategoryCrud = Depends(get_notes_categories_crud),
        settings: Settings = Depends(get_settings),
        validator: Validator = Depends(Validator),
        helper: Helper = Depends(get_helper)
):
    if (
        not data.new_title and
        not data.new_content and
        not data.new_category and
        not data.status
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nothing to update"
        )
    if not data.note_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=m.Error.WRONG_ID.value
        )

    # check if category exist
    note = note_db.get_by_id(note_id=data.note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=m.Error.WRONG_ID.value
        )

    update_fields = {}
    if data.new_title:
        update_fields['title'] = data.new_title
    if data.new_content:
        update_fields['content'] = data.new_content
    if data.new_category:
        category_id = helper.get_category_id_by_name_or_create_new(category_name=data.new_category)
        if not category_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ErrorResponse.CREATING_NOTE_ERROR
            )
        update_fields['category_id'] = category_id

    if data.status:
        update_fields['status'] = data.status

    updated_note_id = note_db.update(
        note_id=note.id,
        field_value=update_fields
    )
    print('updated note id:', updated_note_id)
    if not updated_note_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.UPDATING_NOTE_CATEGORY_ERROR
        )

    return m.UpdateNoteResponse()


@notes_router.post(get_settings().urls.notes_endpoints.delete, name='note: delete')
async def delete_note(
        data: m.DeleteNoteRequest,
        note_db: NotesCrud = Depends(get_notes_crud),
        settings: Settings = Depends(get_settings),
        validator: Validator = Depends(Validator),
):
    note = None
    if data.note_id:
        note = note_db.get_by_id(
            note_id=data.note_id
        )
        if not note:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=m.Error.WRONG_ID.value
            )
    if data.title or data.title == '':
        note = note_db.get_by_title(
            note_title=data.title
        )
        if not note:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=m.Error.WRONG_TITLE.value
            )

    del_messege = note_db.delete(note.id)
    print(del_messege)
    if not del_messege:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse.DELETING_NOTE_ERROR
        )
    return m.DeleteNoteResponse()


@notes_router.post(get_settings().urls.notes_endpoints.get, name='note: get')
async def get_notes(
        data: m.GetNotesRequest,
        note_db: NotesCrud = Depends(get_notes_crud),
        settings: Settings = Depends(get_settings),
        validator: Validator = Depends(Validator),
):
    if data.all:
        notes = note_db.get_all()
        return m.GetNotesResponse(total_documents=len(notes), result=notes)

    if data.search_query:
        notes = note_db.get_by_query(query=data.search_query)
        return m.GetNotesResponse(total_documents=len(notes), result=notes)

