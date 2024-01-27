from app.domain.abc import NotesDatabaseCrud
from app.domain.notes import note_models as m
from app.domain.helper import get_helper, Helper


class NotesCrud:
    def __init__(self, note_db: NotesDatabaseCrud):
        self.note_db = note_db
        self.helper = get_helper()

    def get_by_id(self, note_id: int):
        field_value = dict(id=note_id)
        user = self.note_db.get(field_value)
        return user

    def get_by_title(self, note_title: str):
        field_value = dict(title=note_title)
        note = self.note_db.get(field_value)
        return note

    def create(self, note_model: m.CreateNoteDbModel):
        note = note_model.model_dump()
        note_id = self.note_db.create(note)
        return note_id

    def update(self, note_id: int, field_value: dict):
        filter_by = dict(id=note_id)
        updated_note_id = self.note_db.update(
            filter_by=filter_by,
            field_value=field_value
        )
        return updated_note_id

    def delete(self, note_id: int):
        try:
            self.note_db.delete(item_id=note_id)
            return f'Item with id: {note_id} has been deleted'
        except Exception as e:
            raise f'Del note error: {e}'

    def get_all(self):
        """all notes from db"""
        notes_object = self.note_db.select(all=True)
        notes = [self.helper.convert_note_to_note_model(note) for note in notes_object]
        print('ALL:', notes)
        return notes

    def get_all_by_user_id(self, user_id):
        """all notes from specific user"""
        return ...

    def get_by_query(self, query: str):
        """searching query across whole notes table"""
        notes_object = self.note_db.select(search_query=query)
        notes = [self.helper.convert_note_to_note_model(note) for note in notes_object]
        print('ALL BY QUERY:', notes)
        return notes

def get_notes_crud():
    return NotesCrud(NotesDatabaseCrud())


def get_test_notes_crud():
    return NotesCrud(NotesDatabaseCrud(tests=True))
