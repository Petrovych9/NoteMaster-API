from typing import Optional

from pydantic import BaseModel
from enum import Enum

from app.domain.base_models import STATUS_OK


class NoteCategoryNamesDefault(Enum):
    personal = 'personal'
    work = 'work'
    ideas = 'ideas'
    shopping_list = 'shopping list'


class CreateNoteCategoryRequest(BaseModel):
    name: NoteCategoryNamesDefault | str
    description: Optional[str] = 'description'


class CreatedNoteCategoryResponse(BaseModel):
    status: str = STATUS_OK
    message: str = f"Category created"


class UpdateCategoryRequest(BaseModel):
    category_name: str
    new_name: Optional[NoteCategoryNamesDefault | str] = None
    new_description: Optional[str] = None


class UpdateCategoryResponse(BaseModel):
    status: str = STATUS_OK
    message: str = f"Category updated"


class DeleteCategoryRequest(BaseModel):
    category: str


class DeleteCategoryResponse(BaseModel):
    status: str = STATUS_OK
    message: str = f"Category deleted"
