class Controller:
    def __init__(self, data_loader, graph_builder, graph_uploader, s3_bucket=None, s3_key=None):
        self.graph_builder = graph_builder
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.graph_uploader = graph_uploader

    def execute(self, existing_filename, new_filename):
        self.graph_uploader.eliminate_existing_graph(existing_filename)
        graph = self.graph_builder.build_graph()
        self.graph_uploader.upload_graph(graph, filename=new_filename)
        return None

