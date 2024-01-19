from app.domain.abc import NoteCategoryDatabaseCrud
from app.domain import note_categories_models as m


class NoteCategoryCrud:
    def __init__(self, note_category_db: NoteCategoryDatabaseCrud):
        self.note_category_db = note_category_db

    def get_by_id(self, category_id: int):
        field_value = dict(id=category_id)
        user = self.note_category_db.get(field_value)
        return user

    def get_by_name(self, category_name: str):
        field_value = dict(name=category_name)
        category = self.note_category_db.get(field_value)
        return category

    def create(self, category_model: m.CreateNoteCategoryRequest):
        category = category_model.model_dump()
        category_id = self.note_category_db.create(category)
        return category_id

    def update(self, category_id: int, field_value: dict):
        filter_by = dict(id=category_id)
        updated_category_id = self.note_category_db.update(
            filter_by=filter_by,
            field_value=field_value
        )
        return updated_category_id

    def delete(self, category_id: int):
        try:
            self.note_category_db.delete(item_id=category_id)
            return f'Item with id: {category_id} has been deleted'
        except Exception:
            raise 'Del category error'


def get_notes_categories_crud():
    return NoteCategoryCrud(NoteCategoryDatabaseCrud())


def get_test_notes_categories_crud():
    return NoteCategoryCrud(NoteCategoryDatabaseCrud(tests=True))
