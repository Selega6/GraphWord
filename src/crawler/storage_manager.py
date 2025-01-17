from abc import ABC, abstractmethod

class BookStorage(ABC):
    @abstractmethod
    def upload_book(self, book_id, content, count):
        pass
