from fastapi import FastAPI, Depends, HTTPException
import uvicorn

class WebService:
    def __init__(self, graph, graph_path_finder):
        self.graph = graph
        self.graph_path_finder = graph_path_finder
        self.app = FastAPI(title="Graph API with In-Memory Graph from S3")
        self.add_routes()

    def get_instance(self):
        return self

    def add_routes(self):
        @self.app.get("/")
        def root():
            return {"message": "Welcome to the Graph API with In-Memory Graph from S3"}

        @self.app.get("/shortest-path/")
        def shortest_path(start: str, end: str, service: "WebService" = Depends(self.get_instance)):
            return service.graph_path_finder.get_shortest_path(start, end)

        @self.app.get("/all-paths/")
        def all_paths(start: str, end: str, service: "WebService" = Depends(self.get_instance)):
            return service.graph_path_finder.all_paths(start, end)

        @self.app.get("/longest-path/")
        def longest_path(service: "WebService" = Depends(self.get_instance)):
            return service.graph_path_finder.longest_path()

        @self.app.get("/clusters/")
        def identify_clusters(service: "WebService" = Depends(self.get_instance)):
            return service.graph_path_finder.identify_clusters()

        @self.app.get("/high-connectivity-nodes/")
        def high_connectivity_nodes(top_n: int = 10, service: "WebService" = Depends(self.get_instance)):
            return service.graph_path_finder.high_connectivity_nodes(top_n)

        @self.app.get("/nodes-by-degree/")
        def select_nodes_by_degree(min_degree: int, max_degree: int = None, service: "WebService" = Depends(self.get_instance)):
            return service.graph_path_finder.select_nodes_by_degree(min_degree, max_degree)

        @self.app.get("/isolated-nodes/")
        def isolated_nodes(service: "WebService" = Depends(self.get_instance)):
            return service.graph_path_finder.isolated_nodes()

        @self.app.get("/all-nodes/")
        def all_nodes(service: "WebService" = Depends(self.get_instance)):
            if service.graph is None:
                raise HTTPException(status_code=500, detail="Graph is not loaded in memory.")
            return {"nodes": list(service.graph.nodes())}

        @self.app.get("/all-edges/")
        def all_edges(service: "WebService" = Depends(self.get_instance)):
            if service.graph is None:
                raise HTTPException(status_code=500, detail="Graph is not loaded in memory.")
            return {"edges": list(service.graph.edges(data=True))}

    def run(self):
        uvicorn.run(self.app, host="0.0.0.0", port=8000)

    def update_graph(self, new_graph):
        self.graph = new_graph
        print("Graph updated successfully.")
