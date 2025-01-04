import networkx as nx
from fastapi import HTTPException

class NxGraphPathFinder:
    def __init__(self, graph):
        self.graph = graph

    def get_shortest_path(self, start, end):
        if self.graph is None:
            raise HTTPException(status_code=500, detail="self.graph is not loaded in memory.")
        try:
            shortest_path = nx.shortest_path(self.graph, start, end, method="dijkstra")
            return {"shortest_path": shortest_path}
        except nx.NetworkXNoPath:
            raise HTTPException(status_code=404, detail="No path found between the nodes.")

    def all_paths(self, start, end):
        if self.graph is None:
            raise HTTPException(status_code=500, detail="Graph is not loaded.")
        try:
            paths = list(nx.all_simple_paths(self.graph, source=start, target=end))
            return {"all_paths": paths}
        except nx.NodeNotFound as e:
            raise HTTPException(status_code=404, detail=f"Node not found: {e}")
        
    def longest_path(self):
        if self.graph is None:
            raise HTTPException(status_code=500, detail="Graph is not loaded.")
        try:
            longest_path = max(nx.all_simple_paths(self.graph), key=len)
            return {"longest_path": longest_path}
        except ValueError:
            raise HTTPException(status_code=404, detail="No valid path found in the graph.")
