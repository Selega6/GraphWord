import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
import networkx as nx
from fastapi import HTTPException
from api.endpoints.nx_graph_path_finder import NxGraphPathFinder


class TestNxGraphPathFinder(unittest.TestCase):
    def setUp(self):
        self.graph = nx.Graph()
        self.graph.add_edges_from([
            ("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"),
            ("F", "G"), ("G", "H")
        ])
        self.graph.add_node("I")  
        self.path_finder = NxGraphPathFinder(self.graph)

    def test_initialization(self):
        self.assertEqual(self.path_finder.graph, self.graph)

    def test_get_shortest_path(self):
        result = self.path_finder.get_shortest_path("A", "E")
        self.assertEqual(result, {"shortest_path": ["A", "B", "C", "D", "E"]})

    def test_get_shortest_path_no_path(self):
        with self.assertRaises(HTTPException) as context:
            self.path_finder.get_shortest_path("A", "F")
        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "No path found between the nodes.")

    def test_get_shortest_path_node_not_found(self):
        with self.assertRaises(HTTPException) as context:
            self.path_finder.get_shortest_path("A", "Z")
        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Node not found: Either source A or target Z is not in G")

    def test_all_paths(self):
        response = self.path_finder.all_paths("A", "E")
        expected_response = {
            "all_paths": [["A", "B", "C", "D", "E"]],
            "note": "Limited to 100 paths with a cutoff of 10."
        }
        self.assertEqual(response, expected_response)

    def test_identify_clusters(self):
        result = self.path_finder.identify_clusters()
        expected_clusters = [{"clusters": [["A", "B", "C", "D", "E"], ["F", "G", "H"], ["I"]]}]

        for cluster in result["clusters"]:
            self.assertIn(sorted(cluster), [sorted(c) for c in expected_clusters[0]["clusters"]])

    def test_high_connectivity_nodes(self):
        result = self.path_finder.high_connectivity_nodes(top_n=2)
        self.assertEqual(
            result,
            {"high_connectivity_nodes": [{"node": "B", "degree": 2}, {"node": "C", "degree": 2}]}
        )

    def test_select_nodes_by_degree(self):
        result = self.path_finder.select_nodes_by_degree(min_degree=2)
        self.assertEqual(result, {"selected_nodes": ["B", "C", "D", "G"]})

    def test_isolated_nodes(self):
        result = self.path_finder.isolated_nodes()
        self.assertEqual(result, {"isolated_nodes": ["I"]})
