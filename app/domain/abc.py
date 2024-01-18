from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError, DataError, DBAPIError

from app.db import DatabaseSessionManager
from app.models import Base, User, Note, AuthToken, NoteCategory


class ABCCrud(ABC):

    @abstractmethod
    def get(self, *args, **kwargs):
        """Get an item by ID."""
        raise NotImplementedError

    @abstractmethod
    def create(self, *args, **kwargs):
        """Create a new item."""
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs):
        """Update an item by ID."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args, **kwargs):
        """Delete an item by ID."""
        raise NotImplementedError


class DatabaseCrud(ABCCrud):
    table: Type[Base] = None

    def __init__(self, tests: bool = False):
        self.tests = tests

    def get(self, field_value: dict):
        with DatabaseSessionManager(self.tests) as session:
            q = select(self.table).filter_by(**field_value)
            res = session.execute(q)
            return res.scalar()

    def create(self, data: dict):
        try:
            with DatabaseSessionManager(self.tests) as session:
                item = self.table(**data)
                session.add(item)
                session.commit()
                return item.id

        except IntegrityError as e:
            raise IntegrityError(f"IntegrityError: {e}")
        except DataError as e:
            raise DataError(f"DataError: issue with the data you are trying to insert |  {e}")
        except DBAPIError as e:
            raise DBAPIError(f"DBAPIError: raised for issues such as connection problems | {e}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

    def update(self, filter_by: dict, field_value: dict):
        with DatabaseSessionManager(self.tests) as session:
            q = update(self.table).filter_by(**filter_by).values(**field_value).returning(self.table.id)
            res = session.execute(q)
            res = res.fetchone()
            session.commit()

            return res

    def delete(self, item_id: int):
        with DatabaseSessionManager(self.tests) as session:
            q = delete(self.table).filter_by(id=item_id)
            res = session.execute(q)
            session.commit()

            return res


class UsersDatabaseCrud(DatabaseCrud):
    table = User


class NotesDatabaseCrud(DatabaseCrud):
    table = Note


class NoteCategoryDatabaseCrud(DatabaseCrud):
    table = NoteCategory


class AuthTokenDatabaseCrud(DatabaseCrud):
    table = AuthToken
