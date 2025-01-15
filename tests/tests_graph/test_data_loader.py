import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
from unittest.mock import patch, mock_open, MagicMock
from src.graph.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="word1 10\nword2 5\n")
    def test_load_words(self, mock_file):
        data_loader = DataLoader(file_path="test_file.txt")
        words_with_counts = data_loader.get_words_with_counts()

        self.assertEqual(words_with_counts, {"word1": 10, "word2": 5})
        mock_file.assert_called_once_with("test_file.txt", "r")

    @patch("builtins.open", new_callable=mock_open, read_data="word1 10\nword2 5\n")
    def test_get_text_file_locally(self, mock_file):
        data_loader = DataLoader(file_path="test_file.txt")
        file_path = data_loader.get_text_file_locally()

        self.assertEqual(file_path, "test_file.txt")
        mock_file.assert_called_once_with("test_file.txt", "r")

    @patch("boto3.client")
    @patch("builtins.open", new_callable=mock_open, read_data="word1 10\nword2 5\n")
    def test_get_text_file_from_s3_bucket(self, mock_file, mock_boto3_client):
        mock_s3_client = MagicMock()
        mock_boto3_client.return_value = mock_s3_client
        mock_s3_client.download_file = MagicMock()

        bucket_name = "test-bucket"
        object_key = "folder/test_file.txt"

        with patch("src.graph.data_loader.DataLoader.__init__", return_value=None):
            data_loader = DataLoader()
            data_loader.s3_bucket = bucket_name
            data_loader.s3_key = object_key

        local_file_name = data_loader.get_text_file_from_s3_bucket(bucket_name, object_key)

        self.assertEqual(local_file_name, "test_file.txt")
        mock_s3_client.download_file.assert_called_once_with(bucket_name, object_key, "test_file.txt")

    @patch("builtins.open", new_callable=mock_open, read_data="word1 10\nword2 5\n")
    @patch("boto3.client")
    def test_initialization_with_s3(self, mock_boto3_client, mock_file):
        mock_s3_client = MagicMock()
        mock_boto3_client.return_value = mock_s3_client

        mock_s3_client.download_file = MagicMock()

        bucket_name = "test-bucket"
        object_key = "folder/test_file.txt"

        data_loader = DataLoader(s3_bucket=bucket_name, s3_key=object_key)

        self.assertEqual(data_loader.words_with_counts, {"word1": 10, "word2": 5})
        mock_s3_client.download_file.assert_called_once_with(bucket_name, object_key, "test_file.txt")
        mock_file.assert_called_once_with("test_file.txt", "r")

    @patch("builtins.open", new_callable=mock_open, read_data="word1 10\nword2 5\n")
    def test_initialization_with_local_file(self, mock_file):
        data_loader = DataLoader(file_path="test_file.txt")

        self.assertEqual(data_loader.words_with_counts, {"word1": 10, "word2": 5})
        mock_file.assert_called_once_with("test_file.txt", "r")
