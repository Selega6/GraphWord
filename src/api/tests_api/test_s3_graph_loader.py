import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
from unittest.mock import MagicMock, patch
import pickle
from api.s3_graph_loader import S3GraphLoader


class TestS3GraphLoader(unittest.TestCase):
    def setUp(self):
        self.s3_bucket = "test-bucket"
        self.graph = {"nodes": ["A", "B"], "edges": [("A", "B")]}
        self.mock_s3_client = MagicMock()

        with patch("boto3.client", return_value=self.mock_s3_client):
            self.loader = S3GraphLoader(s3_bucket=self.s3_bucket)

    def test_initialization(self):
        self.assertEqual(self.loader.s3_bucket, self.s3_bucket)
        self.assertEqual(self.loader.graph, None)
        self.assertEqual(self.loader.s3_client, self.mock_s3_client)

    @patch("pickle.loads", return_value={"nodes": ["A", "B"], "edges": [("A", "B")]})
    def test_load_graph(self, mock_pickle_loads):
        mock_response = MagicMock()
        mock_response['Body'].read.return_value = pickle.dumps(self.graph)
        self.mock_s3_client.get_object.return_value = mock_response

        result = self.loader.load_graph("test_graph.pkl")

        self.assertEqual(result, self.graph)
        self.mock_s3_client.get_object.assert_called_once_with(Bucket=self.s3_bucket, Key="test_graph.pkl")
        mock_pickle_loads.assert_called_once()

    def test_get_graph(self):
        self.loader.graph = self.graph
        result = self.loader.get_graph()
        self.assertEqual(result, self.graph)

    @patch("pickle.loads", return_value={"nodes": ["C"], "edges": []})
    def test_refresh_graph(self, mock_pickle_loads):
        mock_response = MagicMock()
        mock_response['Body'].read.return_value = pickle.dumps({"nodes": ["C"], "edges": []})
        self.mock_s3_client.get_object.return_value = mock_response

        result = self.loader.refresh_graph("new_graph.pkl")

        self.assertEqual(result, {"nodes": ["C"], "edges": []})
        self.assertEqual(self.loader.graph, {"nodes": ["C"], "edges": []})
        self.mock_s3_client.get_object.assert_called_once_with(Bucket=self.s3_bucket, Key="new_graph.pkl")
        mock_pickle_loads.assert_called_once()
