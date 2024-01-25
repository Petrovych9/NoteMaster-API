from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.domain.error_models import STATUS_OK
from app.domain.notes_category.note_categories_models import NoteCategoryNamesDefault


class NoteStatus(str, Enum):
    favorite = 'favorite'
    archived = 'archived'


class CreateNoteRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None


class CreateNoteDbModel(BaseModel):
    title: Optional[str] = ''
    content: Optional[str] = ''
    category_id: Optional[int] = None
    user_id: int


class CreatedNoteResponse(BaseModel):
    status: str = STATUS_OK
    message: str = f"Note created"


class UpdateNoteRequest(BaseModel):
    note_id: Optional[int] = None

    new_title: Optional[str] = None
    new_content: Optional[str] = None
    new_category: Optional[str] | Optional[NoteCategoryNamesDefault] = None


class UpdateNoteResponse(BaseModel):
    status: str = STATUS_OK
    message: str = f"Note updated"


class DeleteNoteRequest(BaseModel):
    title: str = None
    note_id: int = None


class DeleteNoteResponse(BaseModel):
    status: str = STATUS_OK
    message: str = f"Note deleted"


class Error(str, Enum):
    WRONG_TITLE = "Wrong note's title"
    WRONG_ID = "Wrong note's id"
