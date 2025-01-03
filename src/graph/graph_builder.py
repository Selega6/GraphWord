from abc import ABC, abstractmethod

class GraphBuilder(ABC):
    @abstractmethod
    def build_graph(self, books):
        pass


