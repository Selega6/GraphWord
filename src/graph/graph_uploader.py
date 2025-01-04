from abc import ABC, abstractmethod

class GraphUploader(ABC):

    @abstractmethod
    def upload_graph(self, graph, graph_file):
        pass
