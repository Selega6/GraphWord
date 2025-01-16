import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import boto3
import pickle
from api.graph_loader import GraphLoader


class S3GraphLoader(GraphLoader):
    def __init__(self, s3_bucket):
        self.s3_bucket = s3_bucket
        self.s3_client = boto3.client('s3')
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
