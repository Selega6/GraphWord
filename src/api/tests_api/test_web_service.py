import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from api.webservice import WebService


class TestWebService(unittest.TestCase):
    def setUp(self):
        self.mock_graph = MagicMock()
        self.mock_graph_path_finder = MagicMock()

        self.mock_graph.nodes.return_value = ["A", "B", "C"]
        self.mock_graph.edges.return_value = [("A", "B"), ("B", "C")]
        self.mock_graph_path_finder.get_shortest_path.return_value = {"shortest_path": ["A", "C"]}
        self.mock_graph_path_finder.all_paths.return_value = {"all_paths": [["A", "B", "C"]]}
        self.mock_graph_path_finder.longest_path.return_value = {"longest_path": ["A", "B", "C"]}
        self.mock_graph_path_finder.identify_clusters.return_value = {"clusters": [["A", "B", "C"]]}
        self.mock_graph_path_finder.high_connectivity_nodes.return_value = {"high_connectivity_nodes": [{"node": "B", "degree": 2}]}
        self.mock_graph_path_finder.select_nodes_by_degree.return_value = {"selected_nodes": ["A", "B"]}
        self.mock_graph_path_finder.isolated_nodes.return_value = {"isolated_nodes": []}

        self.web_service = WebService(self.mock_graph, self.mock_graph_path_finder)
        self.client = TestClient(self.web_service.app)

    def test_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Welcome to the Graph API with In-Memory Graph from S3"})

    def test_shortest_path(self):
        response = self.client.get("/shortest-path/", params={"start": "A", "end": "C"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"shortest_path": ["A", "C"]})
        self.mock_graph_path_finder.get_shortest_path.assert_called_once_with("A", "C")

    def test_all_paths(self):
        response = self.client.get("/all-paths/", params={"start": "A", "end": "C"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"all_paths": [["A", "B", "C"]]})
        self.mock_graph_path_finder.all_paths.assert_called_once_with("A", "C")

    def test_longest_path(self):
        response = self.client.get("/longest-path/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"longest_path": ["A", "B", "C"]})
        self.mock_graph_path_finder.longest_path.assert_called_once()

    def test_clusters(self):
        response = self.client.get("/clusters/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"clusters": [["A", "B", "C"]]})
        self.mock_graph_path_finder.identify_clusters.assert_called_once()

    def test_high_connectivity_nodes(self):
        response = self.client.get("/high-connectivity-nodes/", params={"top_n": 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"high_connectivity_nodes": [{"node": "B", "degree": 2}]})
        self.mock_graph_path_finder.high_connectivity_nodes.assert_called_once_with(5)

    def test_all_nodes(self):
        response = self.client.get("/all-nodes/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"nodes": ["A", "B", "C"]})

    def test_all_edges(self):
        response = self.client.get("/all-edges/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"edges": [["A", "B"], ["B", "C"]]})

    def test_update_graph(self):
        new_graph = MagicMock()
        new_graph.nodes.return_value = ["X", "Y"]
        new_graph.edges.return_value = [("X", "Y")]

        self.web_service.update_graph(new_graph)

        self.assertEqual(self.web_service.graph, new_graph)
