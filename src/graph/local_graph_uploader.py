from .graph_uploader import GraphUploader
import pickle
import os

class LocalGraphUploader(GraphUploader):
    def __init__(self, folder_name):
        self.folder_name = folder_name.rstrip('/')
        self.create_folder()
        

    def upload_graph(self, graph, filename):
        with open(f"{self.folder_name}/{filename}", "wb") as f:
            pickle.dump(graph, f)

    def create_folder(self):
        try:
            os.makedirs(self.folder_name)
        except FileExistsError:
            pass
    
    def eliminate_existing_graph(self, filename):
        try:
            os.remove(f"{self.folder_name}/{filename}")
        except FileNotFoundError:
            pass