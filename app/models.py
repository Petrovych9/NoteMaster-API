import datetime

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class NoteStatus(Enum):
    personal = 'personal'
    work = 'work'
    ideas = 'ideas'
    shopping_list = 'shopping list'


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    password: Mapped[str]
    nickname: Mapped[str]
    created_at: Mapped[str] = mapped_column(default=datetime.datetime.now(datetime.UTC))


class Note(Base):
    __tablename__ = 'notes'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str]
    content: Mapped[str]
    category: Mapped[str]
    status: Mapped[str] = mapped_column(default=NoteStatus.personal)


class AuthToken(Base):
    __tablename__ = 'auth_token'
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str]
    expire: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[str] = mapped_column(default=datetime.datetime.now(datetime.UTC))
