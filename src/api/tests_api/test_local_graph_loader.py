import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
from unittest.mock import mock_open, patch, MagicMock
import pickle
from api.local_graph_loader import LocalGraphLoader


class TestLocalGraphLoader(unittest.TestCase):
    def setUp(self):
        self.folder_name = "./test_folder"
        self.filename = "test_graph.pkl"
        self.mock_graph = {"nodes": ["A", "B"], "edges": [("A", "B")]}
        self.loader = LocalGraphLoader(folder_name=self.folder_name)

    def test_initialization(self):
        self.assertEqual(self.loader.folder_name, "./test_folder")

    @patch("builtins.open", new_callable=mock_open, read_data=pickle.dumps({"nodes": ["A"], "edges": []}))
    def test_load_graph(self, mock_file):
        result = self.loader.load_graph(self.filename)

        self.assertEqual(result, {"nodes": ["A"], "edges": []})
        mock_file.assert_called_once_with(f"./test_folder/{self.filename}", "rb")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_graph_file_not_found(self, mock_file):
        with self.assertRaises(FileNotFoundError):
            self.loader.load_graph(self.filename)

    @patch("builtins.open", new_callable=mock_open, read_data=b"invalid data")
    def test_load_graph_invalid_file(self, mock_file):
        with self.assertRaises(pickle.UnpicklingError):
            self.loader.load_graph(self.filename)
