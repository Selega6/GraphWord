import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
from unittest.mock import patch, MagicMock
import io
import pickle
from src.graph.s3_graph_uploader import S3GraphUploader

class TestS3GraphUploader(unittest.TestCase):
    def setUp(self):
        self.bucket_name = "test-bucket"
        self.region_name = "us-east-1"
        self.folder_name = "test-folder"
        self.graph_file = "test_graph.pkl"
        self.graph = {"nodes": ["a", "b"], "edges": [("a", "b")]}

        self.mock_s3_client = MagicMock()
        with patch("boto3.client", return_value=self.mock_s3_client):
            self.uploader = S3GraphUploader(
                bucket_name=self.bucket_name,
                region_name=self.region_name,
                folder_name=self.folder_name,
                graph_file=self.graph_file,
                graph=self.graph
            )

    def test_initialization(self):
        self.assertEqual(self.uploader.bucket_name, self.bucket_name)
        self.assertEqual(self.uploader.folder_name, self.folder_name)
        self.assertEqual(self.uploader.graph_file, self.graph_file)
        self.assertEqual(self.uploader.graph, self.graph)

    @patch("io.BytesIO")
    def test_upload_graph(self, mock_bytes_io):
        mock_stream = MagicMock()
        mock_bytes_io.return_value = mock_stream
        mock_stream.getvalue.return_value = pickle.dumps(self.graph)

        filename = "uploaded_graph.pkl"
        s3_key = f"{self.folder_name}/{filename}"

        result = self.uploader.upload_graph(self.graph, filename=filename)

        self.mock_s3_client.put_object.assert_called_once_with(
            Bucket=self.bucket_name,
            Key=s3_key,
            Body=mock_stream.getvalue(),
            ContentType='application/octet-stream'
        )
        self.assertEqual(result, s3_key)

    def test_eliminate_existing_graph(self):
        filename = "test_graph.pkl"
        s3_key = f"{self.folder_name}/{filename}"

        result = self.uploader.eliminate_existing_graph(filename=filename)

        self.mock_s3_client.delete_object.assert_called_once_with(
            Bucket=self.bucket_name,
            Key=s3_key
        )
        self.assertIsNone(result)

