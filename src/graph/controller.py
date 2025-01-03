class Controller:
    def __init__(self, data_loader, graph_builder, graph_uploader, s3_bucket=None, s3_key=None):
        self.data_loader = data_loader
        self.graph_builder = graph_builder
        #self.words_with_counts_file = words_with_counts_file
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.graph_uploader = graph_uploader

    def execute(self):
        graph = self.graph_builder.build_graph()
        self.graph_uploader.upload_graph(graph, filename="graph.pkl")
        return None

   