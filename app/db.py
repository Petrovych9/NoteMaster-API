from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


def get_engine(url: str = get_settings().db_url):
    return create_engine(
        url,
        # connect_args={"check_same_thread": False},  # only for SQLite
        echo=False
    )


class DatabaseSessionManager:
    def __init__(self, test=False):
        self.test = test
        self.engine = get_engine()
        self.test_engine = get_engine(get_settings().test_db_url)
        self._sessionmaker = self._get_session()

    def _get_session(self):
        if self.test:
            return sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.test_engine
            )

        return sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    def __enter__(self):
        self.session = self._sessionmaker()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
