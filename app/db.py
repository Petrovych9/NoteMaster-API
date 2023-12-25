from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


def get_engine(url: str = get_settings().db_url):
    return create_engine(
        url,
        connect_args={"check_same_thread": False}  # only for SQLite
    )


def get_db_session():
    session = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return session


def get_test_engine():
    return get_engine(get_settings().test_db_url)


def get_test_session():
    session = sessionmaker(autocommit=False, autoflush=False, bind=get_test_engine())
    return session


def override_get_db_session():
    try:
        test_local_session = get_test_session()
        yield test_local_session()
    finally:
        test_local_session().close()
