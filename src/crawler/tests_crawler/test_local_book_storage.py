import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
from unittest.mock import patch, mock_open
from crawler.local_storage_manager import LocalBookStorage


class TestLocalBookStorage(unittest.TestCase):

    def test_initialization_creates_storage_dir(self):
        with patch("os.makedirs") as mock_makedirs, patch("os.path.exists", return_value=False):
            storage = LocalBookStorage(storage_dir="./test_downloads")
            mock_makedirs.assert_called_once_with("./test_downloads")

    def test_upload_book(self):
        book_id = 123
        content = b"Contenido del libro"
        count = 0
        file_path = "./downloads/pg0.txt"

        with patch("builtins.open", mock_open()) as mock_open_file:
            storage = LocalBookStorage(storage_dir="./downloads")
            storage.upload_book(book_id, content, count)

            mock_open_file.assert_called_once_with(file_path, "wb")
            mock_open_file().write.assert_called_once_with(content)

    def test_delete_all_books(self):
        files = ["pg1.txt", "pg2.txt"]
        with unittest.mock.patch("os.listdir", return_value=files) as mock_listdir, \
            unittest.mock.patch("os.remove") as mock_remove:
            storage = LocalBookStorage(storage_dir="./downloads")
            storage.delete_all_books()

            mock_listdir.assert_called_once_with("./downloads")
            mock_remove.assert_has_calls([
                unittest.mock.call("./downloads/pg1.txt"),
                unittest.mock.call("./downloads/pg2.txt")
            ])
            self.assertEqual(mock_remove.call_count, len(files))

    def test_upload_word_counts(self):
        word_counter = {"word1": 5, "word2": 10}
        output_file = "./word_counts.txt"

        with unittest.mock.patch("builtins.open", unittest.mock.mock_open()) as mock_open:
            storage = LocalBookStorage(output_file=output_file)
            storage.upload_word_counts(word_counter)

            mock_open.assert_called_once_with(output_file, "w", encoding="utf-8")
            mock_open().write.assert_has_calls([
                unittest.mock.call("word1 5\n"),
                unittest.mock.call("word2 10\n")
            ])

    def test_delete_output_file(self):
        with unittest.mock.patch("os.remove") as mock_remove:
            storage = LocalBookStorage(output_file="./word_counts.txt")
            storage.delete_output_file()

            mock_remove.assert_called_once_with("./word_counts.txt")
