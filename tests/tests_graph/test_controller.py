import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
from unittest.mock import MagicMock
from src.graph.controller import Controller

class TestController(unittest.TestCase):
    def setUp(self):
        self.mock_graph_builder = MagicMock()
        self.mock_graph_uploader = MagicMock()
        self.controller = Controller(
            data_loader=None,
            graph_builder=self.mock_graph_builder,
            graph_uploader=self.mock_graph_uploader,
            s3_bucket="test-bucket",
            s3_key="test-key"
        )

    def test_execute_calls_eliminate_existing_graph(self):
        existing_filename = "existing_graph.json"
        new_filename = "new_graph.json"

        self.mock_graph_uploader.eliminate_existing_graph = MagicMock()

        self.controller.execute(existing_filename, new_filename)

        self.mock_graph_uploader.eliminate_existing_graph.assert_called_once_with(existing_filename)

    def test_execute_calls_build_graph(self):
        existing_filename = "existing_graph.json"
        new_filename = "new_graph.json"

        self.mock_graph_builder.build_graph = MagicMock()

        self.controller.execute(existing_filename, new_filename)

        self.mock_graph_builder.build_graph.assert_called_once()

    def test_execute_calls_upload_graph(self):
        existing_filename = "existing_graph.json"
        new_filename = "new_graph.json"

        mock_graph = {"nodes": ["a", "b"], "edges": [("a", "b")]}
        self.mock_graph_builder.build_graph.return_value = mock_graph

        self.mock_graph_uploader.upload_graph = MagicMock()

        self.controller.execute(existing_filename, new_filename)

        self.mock_graph_uploader.upload_graph.assert_called_once_with(mock_graph, filename=new_filename)
