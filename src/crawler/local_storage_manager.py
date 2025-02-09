import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import os
from crawler.storage_manager import BookStorage

class LocalBookStorage(BookStorage):
    def __init__(self, storage_dir="./downloads", output_file="./word_counts.txt"):
        self.storage_dir = storage_dir
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
        self.output_file = output_file

    def upload_book(self, book_id, content, count):
        file_path = os.path.join(self.storage_dir, f"pg{count}.txt")
        try:
            with open(file_path, "wb") as file:
                file.write(content)
        except Exception as e:
            print(f"Error saving the book pg{book_id} locally: {e}")

    def delete_all_books(self):
        try:
            for file_name in os.listdir(self.storage_dir):
                file_path = os.path.join(self.storage_dir, file_name)
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting local books: {e}")

    def upload_word_counts(self, word_counter):
        with open(self.output_file, "w", encoding="utf-8") as file:
            for word, count in word_counter.items():
                file.write(f"{word} {count}\n")
        print(f"Word counts saved to {self.output_file}")

    def delete_output_file(self):
        try:
            os.remove(self.output_file)
        except Exception as e:
            print(f"Error deleting the word count file: {e}")