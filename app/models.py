from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Enum

from app.db import Base


# todo fix creating models according to sqlalchemy


class NoteStatus(Enum):
    personal = 'personal'
    work = 'work'
    ideas = 'ideas'
    shopping_list = 'shopping list'


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    nickname = Column(String)
    created_at = Column(String, default=datetime.now())


class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    content = Column(String)
    category = Column(String)
    status = Column(String, default=NoteStatus.personal)


class AuthToken(Base):
    __tablename__ = 'auth_token'
    id = Column(Integer, primary_key=True)
    token = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(String, default=datetime.now())


class ErrorResponse(str, Enum):
    INVALID_EMAIL = 'INVALID_EMAIL'
    INVALID_PASSWORD = 'INVALID_PASSWORD'
    INVALID_TOKEN = 'INVALID_TOKEN'
    USER_ALREADY_EXIST = 'USER_ALREADY_EXIST'
    USER_NOT_FOUND = 'USER_NOT_FOUND'
    INTERNAL_ERR0R = 'INTERNAL_ERR0R'

