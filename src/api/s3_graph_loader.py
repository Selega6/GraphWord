import boto3
import pickle
from graph_loader import GraphLoader
import os

class S3GraphLoader(GraphLoader):
    def __init__(self, s3_bucket):
        self.s3_bucket = s3_bucket
        self.s3_client = boto3.client('s3',
                        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"), 
                        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
                        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
                        endpoint_url=f"http://172.20.0.2:4566")
        self.graph = None 

    def load_graph(self, path):
        try:
            response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=path)
            graph_data = response['Body'].read()

            self.graph = pickle.loads(graph_data)
            return self.graph

        except self.s3_client.exceptions.NoSuchKey:
            raise FileNotFoundError(f"The file '{path}' does not exist in the bucket '{self.s3_bucket}'.")
        except Exception as e:
            raise RuntimeError(f"Error loading the graph from S3: {e}")

    def get_graph(self):
        if self.graph is None:
            raise RuntimeError("Graph has not been loaded into memory.")
        return self.graph

    def refresh_graph(self, path):
        try:
            self.graph = None
            print("Existing graph cleared from memory.")

            response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=path)
            graph_data = response['Body'].read()

            self.graph = pickle.loads(graph_data)
            print("New graph loaded into memory.")
            return self.graph

        except self.s3_client.exceptions.NoSuchKey:
            raise FileNotFoundError(f"The file '{path}' does not exist in the bucket '{self.s3_bucket}'.")
        except Exception as e:
            raise RuntimeError(f"Error refreshing the graph from S3: {e}")
