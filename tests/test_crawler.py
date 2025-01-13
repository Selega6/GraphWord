import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import MagicMock, patch
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


if __name__ == "__main__":
    unittest.main()

# class TestStorageManager(unittest.TestCase):

#     def test_save_data(self):
#         manager = storage_manager.StorageManager()
#         result = manager.save_data("key", "value")
#         self.assertTrue(result, "save_data should return True when data is saved")

#     def test_load_data(self):
#         manager = storage_manager.StorageManager()
#         manager.save_data("key", "value")
#         data = manager.load_data("key")
#         self.assertEqual(data, "value", "load_data should retrieve the saved value")

#     def test_load_nonexistent_data(self):
#         manager = storage_manager.StorageManager()
#         data = manager.load_data("nonexistent_key")
#         self.assertIsNone(data, "load_data should return None for nonexistent keys")

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
