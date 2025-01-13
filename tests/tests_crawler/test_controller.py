import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
from unittest.mock import MagicMock, patch, mock_open
from src.crawler import controller
from src.crawler import gutenberg_crawler
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
        self.crawler.download_books = unittest.mock.MagicMock()
        self.processor.process_files = unittest.mock.MagicMock(return_value={"word1": 10, "word2": 5})
        self.crawler.storage.upload_word_counts = unittest.mock.MagicMock()

        instance = controller.Controller(crawler=self.crawler, processor=self.processor)
        instance.download_and_process()

        self.crawler.download_books.assert_called_once()
        self.processor.process_files.assert_called_once()
        self.crawler.storage.upload_word_counts.assert_called_once_with({"word1": 10, "word2": 5})

    def test_delete_downloads_and_output(self):
        self.crawler.storage.delete_all_books = unittest.mock.MagicMock()
        self.crawler.storage.delete_output_file = unittest.mock.MagicMock()

        instance = controller.Controller(crawler=self.crawler, processor=self.processor)
        instance.delete_downloads_and_output()

        self.crawler.storage.delete_all_books.assert_called_once()
        self.crawler.storage.delete_output_file.assert_called_once()

    def test_execute(self):
        instance = controller.Controller(crawler=self.crawler, processor=self.processor)
        instance.delete_downloads_and_output = unittest.mock.MagicMock()
        instance.download_and_process = unittest.mock.MagicMock()

        instance.execute()

        instance.delete_downloads_and_output.assert_called_once()
        instance.download_and_process.assert_called_once()

    def test_execute_schedule(self):
        instance = controller.Controller(crawler=self.crawler, processor=self.processor)
        instance.schedule_downloads = unittest.mock.MagicMock()

        instance.execute_schedule()

        instance.schedule_downloads.assert_called_once()

if __name__ == '__main__':
    unittest.main()
