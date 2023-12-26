from app.domain.abc import ABCCrud


class UsersCrud(ABCCrud):
    def __int__(self):
        ...

    def get_by_id(self, _id):
        ...

    def create(self, data):
        ...

    def update(self, _id, data):
        ...

    def delete(self, _id):
        ...
