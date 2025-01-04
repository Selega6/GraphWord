from fastapi import FastAPI, HTTPException
import boto3
import pickle
import networkx as nx
from src.api.endpoints.nx_graph_path_finder import NxGraphPathFinder

# S3 Configuration
bucket_name = "my-bucket"
file_key = "graphs/my_graph.pkl"
s3 = boto3.client("s3")
GLOBAL_GRAPH = None

# Initialize the FastAPI app
app = FastAPI(title="Graph API with In-Memory Graph Loaded from S3")
graph_path_finder = NxGraphPathFinder(GLOBAL_GRAPH)

@app.get("/")
def root():
    return {"message": "Welcome to the Graph API with In-Memory Graph from S3"}

@app.get("/shortest-path/")
def shortest_path(start: str, end: str):
    return graph_path_finder.get_shortest_path(start, end)

@app.get("/all-nodes/")
def all_nodes():
    if graph is None:
        raise HTTPException(status_code=500, detail="Graph is not loaded in memory.")
    return {"nodes": list(graph.nodes())}

@app.get("/all-edges/")
def all_edges():
    if graph is None:
        raise HTTPException(status_code=500, detail="Graph is not loaded in memory.")
    return {"edges": list(graph.edges(data=True))}
