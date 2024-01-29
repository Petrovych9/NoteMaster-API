from enum import Enum
from typing import Optional, List

from pydantic import BaseModel

from app.domain.base_models import BaseModelResponse, GetBase
from app.domain.notes_category.note_categories_models import NoteCategoryNamesDefault

# TODO: need add data models for others entities


class NoteStatus(str, Enum):
    favorite = 'favorite'
    archived = 'archived'


class Error(str, Enum):
    WRONG_TITLE = "Wrong note's title"
    WRONG_ID = "Wrong note's id"

    GETTING_NOTES_ERROR = "GETTING_NOTES_ERROR"


class NoteModel(BaseModel):
    id: int
    title: Optional[str]
    content: Optional[str]
    category_id: Optional[int] = None
    user_id: int
    status: Optional[NoteStatus] = None


class CreateNoteRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None


class CreateNoteDbModel(BaseModel):
    title: Optional[str] = ''
    content: Optional[str] = ''
    category_id: Optional[int] = None
    user_id: int


class CreatedNoteResponse(BaseModelResponse):
    message: str = f"Note created"


class UpdateNoteRequest(BaseModel):
    note_id: Optional[int] = None

    new_title: Optional[str] = None
    new_content: Optional[str] = None
    new_category: Optional[str] | Optional[NoteCategoryNamesDefault] = None

    status: Optional[NoteStatus] = None


class UpdateNoteResponse(BaseModelResponse):
    message: str = f"Note updated"


class DeleteNoteRequest(BaseModel):
    title: str = None
    note_id: int = None


class DeleteNoteResponse(BaseModelResponse):
    message: str = f"Note deleted"


class GetNotesRequest(BaseModel):
    all: Optional[bool] = False
    search_query: Optional[str] = None


class GetNotesResponse(GetBase):
    result: List[NoteModel]
