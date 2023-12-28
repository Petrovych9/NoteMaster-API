from abc import ABC, abstractmethod

from sqlalchemy import insert, delete, select
from sqlalchemy.schema import Table

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
    table: Table = None

    def get(self, **filters):
        with get_db_session() as session:
            q = select(self.table).filter_by(**filters)
            res = session.execute(q)
            return res.all()

    def create(self, data: dict):
        with get_db_session() as session:
            q = insert(self.table).values(**data).returning(self.table.id)
            res = session.execute(q)
            session.commit()

            return res.scalar_one()

    def update(self, item_id: int, field: str, value):
        with get_db_session() as session:
            item = session.get(self.table, item_id)
            item.field = value
            session.commit()

            return item

    def delete(self, item_id):
        with get_db_session() as session:
            q = delete(self.table).where(self.table.c.id == item_id)
            session.execute(q)
            session.commit()

            return


class UsersDatabaseCrud(DatabaseCrud):
    table = User


class NotesDatabaseCrud(DatabaseCrud):
    table = Note

