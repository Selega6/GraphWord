import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import boto3
from graph.graph_uploader import GraphUploader
import io
import pickle


class S3GraphUploader(GraphUploader):
    def __init__(self, bucket_name, region_name, folder_name, graph_file, graph):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3", region_name=region_name)
        self.folder_name = folder_name.rstrip('/')
        self.graph_file = graph_file
        self.graph = graph

    def upload_graph(self, graph, filename="graph.pkl"):
        byte_stream = io.BytesIO()
        pickle.dump(graph, byte_stream)
        byte_stream.seek(0)

        s3_key = f"{self.folder_name}/{filename}"

        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=byte_stream.getvalue(),
                ContentType='application/octet-stream'
            )
        except Exception as e:
            print(f"Error uploading graph to S3: {e}")
            return None
        return s3_key
    
    def eliminate_existing_graph(self, filename):
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=f"{self.folder_name}/{filename}")
        except Exception as e:
            print(f"Error deleting graph from S3: {e}")
            return None
        return None