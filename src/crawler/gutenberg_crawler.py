import requests
import random
from bs4 import BeautifulSoup
from .crawler_base import Crawler


class Gutenberg_crawler(Crawler):
    BASE_URL = "https://www.gutenberg.org/cache/epub/"
    METADATA_URL = "https://www.gutenberg.org/ebooks/"
    BOOK_ID_RANGE = (1, 75000)

    def __init__(self, book_count=20, storage=None):
        self.book_count = book_count
        self.storage = storage

    def generate_random_book_id(self):
        return random.randint(self.BOOK_ID_RANGE[0], self.BOOK_ID_RANGE[1])

    def is_english(self, book_id):
        metadata_url = f"{self.METADATA_URL}{book_id}"
        try:
            response = requests.get(metadata_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            language_row = soup.find(lambda tag: tag.name == "th" and "Language" in tag.text)
            if language_row:
                language = language_row.find_next("td").text.strip()
                if "English" in language:
                    return True
        except Exception as e:
            print(f"Error checking language for book {book_id}: {e}")
        return False

    def download_book(self, book_id):
        download_url = f"{self.BASE_URL}{book_id}/pg{book_id}.txt"
        try:
            if self.is_english(book_id):
                response = requests.get(download_url, stream=True)
                if response.status_code == 200:
                    if self.storage:
                        self.storage.upload_book(book_id, response.content)
                    return True
        except Exception as e:
            print(f"Error downloading book {book_id}: {e}")
        return False

    def download_books(self):
        downloaded_books = 0
        attempted_books = set()

        while downloaded_books < self.book_count:
            book_id = self.generate_random_book_id()
            
            if book_id in attempted_books:
                continue
            
            attempted_books.add(book_id)

            if self.download_book(book_id):
                downloaded_books += 1
