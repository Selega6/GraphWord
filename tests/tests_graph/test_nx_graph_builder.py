import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
from unittest.mock import MagicMock, patch
import networkx as nx
from src.graph.nx_graph_builder import NxGraphBuilder

class TestNxGraphBuilder(unittest.TestCase):
    def setUp(self):
        self.mock_data_loader = MagicMock()
        self.mock_data_loader.load_words.return_value = {
            "cat": 10,
            "bat": 20,
            "rat": 30,
            "car": 15,
            "bar": 25,
        }
        self.builder = NxGraphBuilder(data_loader=self.mock_data_loader)

    def test_initialization(self):
        self.assertEqual(self.builder.words_with_counts, {
            "cat": 10,
            "bat": 20,
            "rat": 30,
            "car": 15,
            "bar": 25,
        })
        self.assertTrue(isinstance(self.builder.graph, nx.Graph))

    def test_differs_by_one_letter(self):
        self.assertTrue(self.builder.differs_by_one_letter("cat", "bat")) 
        self.assertTrue(self.builder.differs_by_one_letter("bat", "rat")) 
        self.assertTrue(self.builder.differs_by_one_letter("bar", "car")) 
        self.assertFalse(self.builder.differs_by_one_letter("cat", "dog"))
        self.assertTrue(self.builder.differs_by_one_letter("cat", "at"))  

    def test_build_graph(self):
        graph = self.builder.build_graph()

        expected_nodes = {
            "cat": {"frequency": 10},
            "bat": {"frequency": 20},
            "rat": {"frequency": 30},
            "car": {"frequency": 15},
            "bar": {"frequency": 25},
        }
        for node, attributes in expected_nodes.items():
            self.assertIn(node, graph.nodes)
            self.assertEqual(graph.nodes[node], attributes)

        expected_edges = {
            ("cat", "bat"): {"weight": 15.0},
            ("bat", "rat"): {"weight": 25.0},
            ("car", "bar"): {"weight": 20.0},
        }
        for edge, attributes in expected_edges.items():
            self.assertIn(edge, graph.edges)
            self.assertEqual(graph.edges[edge], attributes)

    @patch("networkx.write_gpickle")
    def test_save_graph(self, mock_write_gpickle):
        self.builder.graph = nx.Graph() 
        self.builder.save_graph("test_graph.pkl")

        mock_write_gpickle.assert_called_once_with(self.builder.graph, "test_graph.pkl")
