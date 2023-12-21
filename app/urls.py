from enum import Enum


class BasicUrls(Enum):
    ROOT = '/'
    LOGIN = '/login'


class UserUrls(Enum):
    USER = '/user'
    USERS = '/users'


class NoteUrls(Enum):
    NOTE = '/note'
    NOTES = '/notes'
