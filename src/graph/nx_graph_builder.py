import networkx as nx
from .graph_builder import GraphBuilder


class NxGraphBuilder(GraphBuilder):
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.words_with_counts = self.data_loader.load_words()
        self.graph = nx.Graph()

    def differs_by_one_letter(self, word1, word2):
        len_diff = abs(len(word1) - len(word2))
        if len_diff > 1:
            return False

        if len(word1) == len(word2):
            differences = sum(1 for a, b in zip(word1, word2) if a != b)
            return differences == 1

        if len(word1) > len(word2):
            word1, word2 = word2, word1

        for i in range(len(word2)):
            if word1 == word2[:i] + word2[i+1:]:
                return True

        return False

    def build_graph(self):
        graph = nx.Graph()
        for word, count in self.words_with_counts.items():
            graph.add_node(word, frequency=count)
        
        words = list(self.words_with_counts.keys())
        for i, word1 in enumerate(words):
            for word2 in words[i + 1:]:
                if self.differs_by_one_letter(word1, word2):
                    weight = (self.words_with_counts[word1] + self.words_with_counts[word2]) / 2
                    graph.add_edge(word1, word2, weight=weight)
        return graph
    
    def save_graph(self, filename):
        nx.write_gpickle(self.graph, filename)
        return None
    