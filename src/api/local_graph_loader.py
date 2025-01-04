from graph_loader import GraphLoader

import pickle


class LocalGraphLoader(GraphLoader):
    
    def load_graph(self, path: str):
        with open(path, "rb") as f:
            graph = pickle.load(f)
        return graph
    
    