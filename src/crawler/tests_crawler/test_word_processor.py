from collections import Counter
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
from unittest.mock import patch, MagicMock
from collections import Counter
from crawler.word_processor import WordProcessor


class TestWordProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = WordProcessor(input_dir="test_dir", lower_bound=3, upper_bound=5, s3_bucket="test-bucket")

    def test_initialization(self):
        self.assertEqual(self.processor.input_dir, "test_dir")
        self.assertEqual(self.processor.lower_bound, 3)
        self.assertEqual(self.processor.upper_bound, 5)
        self.assertEqual(self.processor.s3_bucket, "test-bucket")
        self.assertTrue(len(self.processor.stopwords) > 0)

    def test_process_file_content_with_stopwords(self):
        content = "the word1 is a word2"
        result = self.processor.process_file_content(content)
        expected = Counter({"word1": 1, "word2": 1})
        self.assertEqual(result, expected)

    def test_process_file_content_empty_file(self):
        content = ""
        result = self.processor.process_file_content(content)
        self.assertEqual(result, Counter())
