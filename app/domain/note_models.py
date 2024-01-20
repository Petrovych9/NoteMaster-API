from enum import Enum


class NoteStatus(str, Enum):
    favorite = 'favorite'
    archived = 'archived'
