from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from app.config import DATABASE_URL

Base = declarative_base()


def connect_db():
    engine = create_engine(
        DATABASE_URL,
        connect_args={}
    )
    session = Session(bind=engine.connect())
    return session


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
    created_at = Column(String, default=datetime.utcnow())


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
    created_at = Column(String, default=datetime.utcnow())
