from controller import Controller
from data_loader import DataLoader
from nx_graph_builder import NxGraphBuilder
from local_graph_uploader import LocalGraphUploader
from s3_graph_uploader import S3GraphUploader

def main():
    words_with_counts_file = "../crawler/word_counts.txt"
    s3_bucket = None
    s3_key = None
    data_loader = DataLoader(words_with_counts_file, s3_bucket, s3_key)
    graph_builder = NxGraphBuilder(data_loader=data_loader)
    graph_uploader = LocalGraphUploader(folder_name="graphs")
    #s3_graph_uploader = S3GraphUploader(s3_bucket, s3_key)
    controller = Controller(data_loader, graph_builder, graph_uploader)
    existing_graph = "graph.pkl"
    new_graph = "graph.pkl"
    controller.execute(existing_graph, new_graph)


if __name__ == "__main__":
    main()
