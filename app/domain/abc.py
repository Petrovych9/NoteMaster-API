from abc import ABC, abstractmethod


class ABCCrud(ABC):

    @abstractmethod
    def get_by_id(self, _id):
        """Get an item by ID."""
        pass

    @abstractmethod
    def create(self, data):
        """Create a new item."""
        pass

    @abstractmethod
    def update(self, _id, data):
        """Update an item by ID."""
        pass

    @abstractmethod
    def delete(self, _id):
        """Delete an item by ID."""
        pass

