from abc import ABC, abstractmethod

class Crawler(ABC):
    @abstractmethod
    def download_book(self, book_id):
        pass

    @abstractmethod
    def download_books(self):
        pass