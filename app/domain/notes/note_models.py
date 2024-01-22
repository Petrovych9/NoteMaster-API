from enum import Enum

from pydantic import BaseModel

from app.domain.error_models import STATUS_OK


class NoteStatus(str, Enum):
    favorite = 'favorite'
    archived = 'archived'


class CreateNoteRequest(BaseModel):
    title: str = None
    content: str = None


class CreatedNoteResponse(BaseModel):
    status: str = STATUS_OK
    message: str = f"Note created"
