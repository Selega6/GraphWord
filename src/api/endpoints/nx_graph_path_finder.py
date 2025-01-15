import networkx as nx
from fastapi import HTTPException

class NxGraphPathFinder:
    def __init__(self, graph):
        self.graph = graph

    def get_shortest_path(self, start, end):
        if self.graph is None:
            raise HTTPException(status_code=500, detail="Graph is not loaded.")
        try:
            shortest_path = nx.shortest_path(self.graph, source=start, target=end, method="dijkstra")
            return {"shortest_path": shortest_path}
        except nx.NetworkXNoPath:
            raise HTTPException(status_code=404, detail="No path found between the nodes.")
        except nx.NodeNotFound as e:
            raise HTTPException(status_code=404, detail=f"Node not found: {e}")

    def all_paths(self, start, end, max_paths=100, cutoff=10):
        if self.graph is None:
            raise HTTPException(status_code=500, detail="Graph is not loaded.")
        try:
            paths_generator = nx.all_simple_paths(self.graph, source=start, target=end, cutoff=cutoff)
            paths = []
            for i, path in enumerate(paths_generator):
                if i >= max_paths:
                    break
                paths.append(path)
            return {"all_paths": paths, "note": f"Limited to {max_paths} paths with a cutoff of {cutoff}."}
        except nx.NodeNotFound as e:
            raise HTTPException(status_code=404, detail=f"Node not found: {e}")

    def longest_path(self, cutoff=20):
        if self.graph is None:
            raise HTTPException(status_code=500, detail="Graph is not loaded.")
        try:
            longest_path = []
            for source in self.graph.nodes:
                for target in self.graph.nodes:
                    if source != target:
                        paths = nx.all_simple_paths(self.graph, source=source, target=target, cutoff=cutoff)
                        for path in paths:
                            if len(path) > len(longest_path):
                                longest_path = path
            return {"longest_path": longest_path, "note": f"Search limited to paths with a cutoff of {cutoff}."}
        except ValueError:
            raise HTTPException(status_code=404, detail="No valid path found in the graph.")

    def identify_clusters(self):
        if self.graph is None:
            raise HTTPException(status_code=500, detail="Graph is not loaded.")
        clusters = list(nx.connected_components(self.graph))
        return {"clusters": [list(cluster) for cluster in clusters]}

    def high_connectivity_nodes(self, top_n=10):
        if self.graph is None:
            raise HTTPException(status_code=500, detail="Graph is not loaded.")
        degrees = sorted(self.graph.degree(), key=lambda x: x[1], reverse=True)
        top_nodes = [{"node": node, "degree": degree} for node, degree in degrees[:top_n]]
        return {"high_connectivity_nodes": top_nodes}

    def select_nodes_by_degree(self, min_degree, max_degree=None):
        if self.graph is None:
            raise HTTPException(status_code=500, detail="Graph is not loaded.")
        selected_nodes = [
            node for node, degree in self.graph.degree()
            if degree >= min_degree and (max_degree is None or degree <= max_degree)
        ]
        return {"selected_nodes": selected_nodes}

    def isolated_nodes(self):
        if self.graph is None:
            raise HTTPException(status_code=500, detail="Graph is not loaded.")
        isolates = list(nx.isolates(self.graph))
        return {"isolated_nodes": isolates}
