import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from api.graph_loader import GraphLoader
import pickle


class LocalGraphLoader(GraphLoader):
    def __init__(self, folder_name):
        self.folder_name = folder_name.rstrip('/')
    
    def load_graph(self, filename: str):
        with open(f"{self.folder_name}/{filename}", "rb") as f:
            return pickle.load(f)
