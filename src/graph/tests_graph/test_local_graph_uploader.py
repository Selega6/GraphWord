import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import pickle
from graph.local_graph_uploader import LocalGraphUploader

class TestLocalGraphUploader(unittest.TestCase):
    @patch("os.makedirs")
    def test_create_folder(self, mock_makedirs):
        uploader = LocalGraphUploader(folder_name="./test_folder")
        mock_makedirs.assert_called_once_with("./test_folder")

    @patch("os.makedirs", side_effect=FileExistsError)
    def test_create_folder_existing(self, mock_makedirs):
        uploader = LocalGraphUploader(folder_name="./test_folder")
        mock_makedirs.assert_called_once_with("./test_folder")

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_upload_graph(self, mock_makedirs, mock_file):
        uploader = LocalGraphUploader(folder_name="./test_folder")
        mock_graph = {"nodes": ["a", "b"], "edges": [("a", "b")]}
        uploader.upload_graph(mock_graph, filename="test_graph.pkl")

        mock_file.assert_called_once_with("./test_folder/test_graph.pkl", "wb")
        mock_file().write.assert_called_once()

    @patch("os.remove")
    def test_eliminate_existing_graph(self, mock_remove):
        uploader = LocalGraphUploader(folder_name="./test_folder")
        uploader.eliminate_existing_graph(filename="test_graph.pkl")

        mock_remove.assert_called_once_with("./test_folder/test_graph.pkl")

    @patch("os.remove", side_effect=FileNotFoundError)
    def test_eliminate_existing_graph_nonexistent(self, mock_remove):
        uploader = LocalGraphUploader(folder_name="./test_folder")
        uploader.eliminate_existing_graph(filename="test_graph.pkl")

        mock_remove.assert_called_once_with("./test_folder/test_graph.pkl")
