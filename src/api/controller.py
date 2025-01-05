from webservice import WebService
import threading
import time
from endpoints.nx_graph_path_finder import NxGraphPathFinder

class Controller:
    def __init__(self, graph_filename, graph_loader):
        self.graph_loader = graph_loader
        self.graph = self.graph_loader.load_graph(graph_filename)
        self.graph_path_finder = NxGraphPathFinder(self.graph)
        self.webservice = WebService(self.graph, self.graph_path_finder)
        self.graph_filename = graph_filename
        self.lock = threading.Lock()

    def execute(self):
        threading.Thread(target=self.webservice.run, daemon=True).start()

    def reload_graph_for_webservice(self):
        with self.lock:
            self.graph = self.graph_loader.load_graph(self.graph_filename)
            self.webservice.update_graph(self.graph)