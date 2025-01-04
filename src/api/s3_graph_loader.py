import boto3
import pickle
from graph_loader import GraphLoader


class S3GraphLoader(GraphLoader):
    def __init__(self, s3_bucket):
        self.s3_bucket = s3_bucket
        self.s3_client = boto3.client('s3')

    def load_graph(self, path):
        global GLOBAL_GRAPH

        try:
            response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=path)
            graph_data = response['Body'].read()

            GLOBAL_GRAPH = pickle.loads(graph_data)
            return GLOBAL_GRAPH

        except self.s3_client.exceptions.NoSuchKey:
            raise FileNotFoundError(f"The file '{path}' does not exist in the bucket '{self.s3_bucket}'.")
        except Exception as e:
            raise RuntimeError(f"Error loading the graph from S3: {e}")

    def get_graph(self):
        global GLOBAL_GRAPH

        if GLOBAL_GRAPH is None:
            raise RuntimeError("Graph has not been loaded into memory.")
        return GLOBAL_GRAPH

    def refresh_graph(self, path):
        global GLOBAL_GRAPH

        try:
            GLOBAL_GRAPH = None
            print("Existing graph cleared from memory.")

            response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=path)
            graph_data = response['Body'].read()

            GLOBAL_GRAPH = pickle.loads(graph_data)
            print("New graph loaded into memory.")
            return GLOBAL_GRAPH

        except self.s3_client.exceptions.NoSuchKey:
            raise FileNotFoundError(f"The file '{path}' does not exist in the bucket '{self.s3_bucket}'.")
        except Exception as e:
            raise RuntimeError(f"Error refreshing the graph from S3: {e}")
