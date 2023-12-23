from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import DATABASE_URL, DATABASE_URL_TEST


class Base(DeclarativeBase):
    pass


def get_engine(url: str = DATABASE_URL):
    return create_engine(
        url,
        connect_args={"check_same_thread": False}  # only for SQLite
    )


def get_db_session(engine):
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session


def get_test_engine():
    return get_engine(DATABASE_URL_TEST)


def get_test_session():
    return get_db_session(get_test_engine())


def override_get_db_session():
    try:
        test_local_session = get_test_session()
        yield test_local_session()
    finally:
        test_local_session().close()
