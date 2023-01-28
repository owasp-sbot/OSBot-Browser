from osbot_plotly.NX_DiGraph import NX_DiGraph
from osbot_plotly.NX_Graph import NX_Graph
from osbot_utils.utils.Files import file_create_bytes

class Plotly_Base:

    def __init__(self, use_digraph=True):
        self.figure                      = None
        self.jpg_scale                   = 1.0
        self.jpg_path                    = f"/tmp/plotly.jpg"
        self.title                       = 'Plotly Diagram'
        self.use_digraph                 = use_digraph
        self.nx_graph                    = None
        self.new_nx_graph()


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def new_nx_graph(self):
        if self.use_digraph:
            self.nx_graph = NX_DiGraph()
        else:
            self.nx_graph = NX_Graph()
        return self.nx_graph

    def save_as_jpg(self):
        if self.figure:
            image_bytes = self.figure.to_image(format='jpg', scale=self.jpg_scale)
            file_create_bytes(path=self.jpg_path, bytes=image_bytes)
        return self

    def set_figure(self, figure):
        self.figure = figure

    def set_graph(self, nx_graph):
        if nx_graph is not None:
            self.nx_graph = nx_graph
        return self

    def set_title(self, title):
        self.title = title
        return self
