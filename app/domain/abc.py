from abc import ABC, abstractmethod

from sqlalchemy import insert, delete, select, update
from typing import Type

from sqlalchemy.exc import IntegrityError, DataError, DBAPIError

from app.models import Base

from app.db import get_db_session
from app.models import User, Note


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

    def get(self, field_value: dict):
        with get_db_session() as session:
            q = select(self.table).filter_by(**field_value)
            res = session.execute(q)
            return res.scalar()

    def create(self, data: dict):
        try:
            with get_db_session() as session:
                item = self.table(**data)
                session.add(item)
                session.commit()
                return item.id

        except IntegrityError as e:
            raise f"IntegrityError: {e}"
        except DataError as e:
            raise f"DataError: issue with the data you are trying to insert |  {e}"
        except DBAPIError as e:
            raise f"DBAPIError: raised for issues such as connection problems | {e}"
        except Exception as e:
            raise f"Unexpected error: {e}"

    def update(self, item_id: int, field_value: dict):
        with get_db_session() as session:
            q = update(self.table).filter_by(id=item_id).values(**field_value).returning(self.table.id)
            res = session.execute(q)
            res = res.fetchone()
            session.commit()

            return res

    def delete(self, item_id: int):
        with get_db_session() as session:
            q = delete(self.table).filter_by(id=item_id)
            res = session.execute(q)
            session.commit()

            return res


class UsersDatabaseCrud(DatabaseCrud):
    table = User


class NotesDatabaseCrud(DatabaseCrud):
    table = Note
