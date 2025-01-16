import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
from unittest.mock import MagicMock, patch
from api.controller import Controller


class TestController(unittest.TestCase):
    def setUp(self):
        self.mock_graph_loader = MagicMock()
        self.mock_graph_loader.load_graph.return_value = {"nodes": ["a", "b"], "edges": [("a", "b")]}
        self.mock_webservice = MagicMock()
        self.mock_graph_path_finder = MagicMock()

        patch("api.controller.WebService", return_value=self.mock_webservice).start()
        patch("api.controller.NxGraphPathFinder", return_value=self.mock_graph_path_finder).start()

        self.controller = Controller(graph_filename="test_graph.pkl", graph_loader=self.mock_graph_loader)

    def tearDown(self):
        patch.stopall()

    def test_initialization(self):
        self.mock_graph_loader.load_graph.assert_called_once_with("test_graph.pkl")
        self.assertEqual(self.controller.graph, {"nodes": ["a", "b"], "edges": [("a", "b")]})
        self.assertEqual(self.controller.graph_path_finder, self.mock_graph_path_finder)
        self.assertEqual(self.controller.webservice, self.mock_webservice)
        self.assertEqual(self.controller.graph_filename, "test_graph.pkl")

    @patch("threading.Thread")
    def test_execute(self, mock_thread):
        self.controller.execute()

        mock_thread.assert_called_once_with(target=self.mock_webservice.run, daemon=True)
        mock_thread.return_value.start.assert_called_once()

    @patch("api.controller.Controller.__init__", return_value=None)
    @patch("threading.Lock", return_value=MagicMock())
    def test_reload_graph_for_webservice(self, mock_lock, mock_init):
        controller = Controller.__new__(Controller)
        controller.graph_loader = self.mock_graph_loader
        controller.webservice = self.mock_webservice
        controller.graph_filename = "test_graph.pkl"
        controller.lock = mock_lock 

        self.mock_graph_loader.reset_mock()

        new_graph = {"nodes": ["x", "y"], "edges": [("x", "y")]}
        self.mock_graph_loader.load_graph.return_value = new_graph

        controller.reload_graph_for_webservice()

        self.mock_graph_loader.load_graph.assert_called_once_with("test_graph.pkl")

        self.mock_webservice.update_graph.assert_called_once_with(new_graph)

        mock_lock.__enter__.assert_called_once()
        mock_lock.__exit__.assert_called_once()

    @patch("threading.Lock")
    def test_reload_graph_thread_safety(self, mock_lock):
        mock_lock_instance = mock_lock.return_value
        controller = Controller.__new__(Controller) 
        controller.graph_loader = self.mock_graph_loader
        controller.webservice = self.mock_webservice
        controller.graph_filename = "test_graph.pkl"
        controller.lock = mock_lock_instance

        controller.reload_graph_for_webservice()

        mock_lock_instance.__enter__.assert_called_once()
        mock_lock_instance.__exit__.assert_called_once()
