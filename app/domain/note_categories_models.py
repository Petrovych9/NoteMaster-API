from typing import Optional

from pydantic import BaseModel
from enum import Enum

from app.domain.error_models import STATUS_OK


class NoteNamesDefault(Enum):
    personal = 'personal'
    work = 'work'
    ideas = 'ideas'
    shopping_list = 'shopping list'


class CreateNoteCategoryRequest(BaseModel):
    name: Optional[NoteNamesDefault | str] = NoteNamesDefault.personal.value
    description: Optional[str]


class CreatedNoteCategoryResponse(BaseModel):
    status: str = STATUS_OK
    message: str = f"Category created"


class UpdateCategoryRequest(BaseModel):
    category: str
    new_name: Optional[NoteNamesDefault | str]
    new_description: Optional[str]


class UpdateCategoryResponse(BaseModel):
    status: str = STATUS_OK
    message: str = f"Category updated"


class DeleteCategoryRequest(BaseModel):
    category: str


class DeleteCategoryResponse(BaseModel):
    status: str = STATUS_OK
    message: str = f"Category deleted"
