from collections import Counter
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
from unittest.mock import MagicMock, patch, mock_open
from src.crawler import controller
from src.crawler import gutenberg_crawler
from src.crawler import storage_manager
from src.crawler import word_processor
from src.crawler.local_storage_manager import LocalBookStorage
from src.crawler.word_processor import WordProcessor


class TestWordProcessor(unittest.TestCase):

    def test_initialization(self):
        processor = WordProcessor(input_dir="./input", output_file="./output.txt", lower_bound=4, upper_bound=8)
        self.assertEqual(processor.input_dir, "./input")
        self.assertEqual(processor.output_file, "./output.txt")
        self.assertEqual(processor.lower_bound, 4)
        self.assertEqual(processor.upper_bound, 8)
        self.assertIn("the", processor.stop_words)

if __name__ == "__main__":
    unittest.main()