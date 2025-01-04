from abc import ABC, abstractmethod

class GraphLoader(ABC):
    @abstractmethod
    def load_graph(self, path: str):
        pass