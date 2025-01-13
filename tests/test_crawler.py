import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import MagicMock, patch, mock_open
from src.crawler import controller
from src.crawler import gutenberg_crawler
from src.crawler import storage_manager
from src.crawler import word_processor
from src.crawler.local_storage_manager import LocalBookStorage


class TestCrawlerController(unittest.TestCase):

    def setUp(self):
        self.input_dir = "./downloads"
        self.output_file = "./word_counts.txt"
        self.lower_bound = 3
        self.upper_bound = 5
        self.storage = LocalBookStorage()
        self.crawler = gutenberg_crawler.Gutenberg_crawler(20, self.storage)
        self.processor = word_processor.WordProcessor(
            self.input_dir, 
            self.output_file, 
            self.lower_bound, 
            self.upper_bound
        )

    def test_initialization(self):
        instance = controller.Controller(crawler=self.crawler, processor=self.processor)
        self.assertIsNotNone(instance, "Controller instance should be initialized")

    def test_download_and_process(self):
        """Prueba que download_and_process ejecuta las acciones esperadas."""
        self.crawler.download_books = unittest.mock.MagicMock()
        self.processor.process_files = unittest.mock.MagicMock(return_value={"word1": 10, "word2": 5})
        self.crawler.storage.upload_word_counts = unittest.mock.MagicMock()

        instance = controller.Controller(crawler=self.crawler, processor=self.processor)
        instance.download_and_process()

        self.crawler.download_books.assert_called_once()
        self.processor.process_files.assert_called_once()
        self.crawler.storage.upload_word_counts.assert_called_once_with({"word1": 10, "word2": 5})

    def test_delete_downloads_and_output(self):
        """Prueba que delete_downloads_and_output elimina los libros y el archivo de salida."""
        self.crawler.storage.delete_all_books = unittest.mock.MagicMock()
        self.crawler.storage.delete_output_file = unittest.mock.MagicMock()

        instance = controller.Controller(crawler=self.crawler, processor=self.processor)
        instance.delete_downloads_and_output()

        self.crawler.storage.delete_all_books.assert_called_once()
        self.crawler.storage.delete_output_file.assert_called_once()

    def test_execute(self):
        """Prueba que execute llama a delete_downloads_and_output y download_and_process."""
        instance = controller.Controller(crawler=self.crawler, processor=self.processor)
        instance.delete_downloads_and_output = unittest.mock.MagicMock()
        instance.download_and_process = unittest.mock.MagicMock()

        instance.execute()

        instance.delete_downloads_and_output.assert_called_once()
        instance.download_and_process.assert_called_once()

    def test_execute_schedule(self):
        """Prueba que execute_schedule llama a schedule_downloads."""
        instance = controller.Controller(crawler=self.crawler, processor=self.processor)
        instance.schedule_downloads = unittest.mock.MagicMock()

        instance.execute_schedule()

        instance.schedule_downloads.assert_called_once()


class TestLocalBookStorage(unittest.TestCase):
    def test_initialization_creates_storage_dir(self):
        with patch("os.makedirs") as mock_makedirs, patch("os.path.exists", return_value=False):
            storage = LocalBookStorage(storage_dir="./test_downloads")
            mock_makedirs.assert_called_once_with("./test_downloads")

    def test_upload_book(self):
        book_id = 123
        content = b"Contenido del libro"
        file_path = "./downloads/pg123.txt"

        with patch("builtins.open", mock_open()) as mock_open_file:
            storage = LocalBookStorage(storage_dir="./downloads")
            storage.upload_book(book_id, content)

            mock_open_file.assert_called_once_with(file_path, "wb")
            mock_open_file().write.assert_called_once_with(content)

    def test_delete_all_books(self):
        """Prueba que delete_all_books elimina todos los libros."""
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
        """Prueba que upload_word_counts guarda los conteos de palabras correctamente."""
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
        """Prueba que delete_output_file elimina el archivo de salida."""
        with unittest.mock.patch("os.remove") as mock_remove:
            storage = LocalBookStorage(output_file="./word_counts.txt")
            storage.delete_output_file()

            mock_remove.assert_called_once_with("./word_counts.txt")


if __name__ == "__main__":
    unittest.main()

# class TestGutenbergCrawler(unittest.TestCase):

#     def test_fetch_data(self):
#         crawler = gutenberg_crawler.Gutenberg_crawler()
#         data = crawler.fetch_data("http://example.com")
#         self.assertIsInstance(data, str, "fetch_data should return a string of data")

#     def test_fetch_data_invalid_url(self):
#         crawler = gutenberg_crawler.Gutenberg_crawler()
#         with self.assertRaises(ValueError):
#             crawler.fetch_data("invalid_url")

# class TestWordProcessor(unittest.TestCase):

#     def test_process_word(self):
#         processor = word_processor.WordProcessor()
#         result = processor.process_word("example")
#         self.assertEqual(result, "EXAMPLE", "process_word should convert word to uppercase")

#     def test_process_empty_string(self):
#         processor = word_processor.WordProcessor()
#         result = processor.process_word("")
#         self.assertEqual(result, "", "process_word should return an empty string for input \"\"")
