from pydantic import BaseModel
from enum import Enum


class Category(Enum):
    personal = 'personal'
    work = 'work'
    ideas = 'ideas'
    shopping_list = 'shopping list'


class Note(BaseModel):
    title: str
    content: str | None = None
    category_id: int | None = None
    user_id: int
