from fastapi import FastAPI, HTTPException
import boto3
import threading
import time
from endpoints.nx_graph_path_finder import NxGraphPathFinder
from local_graph_loader import LocalGraphLoader
from controller import Controller


def periodically_reload_graph(controller, interval_seconds):
    while True:
        time.sleep(interval_seconds)
        try:
            controller.reload_graph_for_webservice()
        except Exception as e:
            print(f"Error reloading graph: {e}")


def main():
    # S3 Configuration
    bucket_name = "my-bucket"
    file_key = "graphs/my_graph.pkl"
    folder_name = "../graph/graphs"
    graph_filename = "graph.pkl"
    graph_loader = LocalGraphLoader(folder_name=folder_name)
    controller = Controller(graph_loader=graph_loader, graph_filename=graph_filename)

    controller.execute()

    reload_interval = 24 * 60 * 60 
    threading.Thread(target=periodically_reload_graph, args=(controller, reload_interval), daemon=True).start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
