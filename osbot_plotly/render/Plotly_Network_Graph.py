import plotly.graph_objects as go
import networkx as nx

from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Files import file_create_bytes


class Plotly_Network_Graph:

    def __init__(self):
        self.figure                      = None
        self.nx_graph                    = None
        self.png_path                    = f"/tmp/plotly.jpg"
        self.title                       = 'Plotly Graph'
        self.nx_positions                = None
        self.nx_spring_layout_k          = 1.00
        self.nx_spring_layout_iterations = 50# 500
        self.pl_edge_width               = 0.5
        self.pl_edge_color               = '#888'
        self.pl_edge_shape               = 'spline'
        self.pl_edge_text_color          = 'black'
        self.pl_edge_text_size           = 7
        self.pl_node_text_size           = 6
        self.pl_node_mode                = 'markers+text'
        self.pl_node_text_position       = "top center"
        self.pl_node_show_scale          = False
        self.pl_node_size                = 6
        self.pl_node_color               = "black"
        self.pl_show_legend              = False
        self.pl_edges_lines              = None
        self.pl_edges_texts              = None
        self.pl_nodes                    = None


    def nx_create_positions_from_graph(self):
        self.nx_positions = nx.spring_layout(self.nx_graph, k=self.nx_spring_layout_k, iterations=self.nx_spring_layout_iterations)
        return self

    def assign_positions_to_graph(self):
        for n, p in self.nx_positions.items():
            self.nx_graph.nodes[n]['pos'] = p
        return self

    def pl_create_edges_lines(self):
        kwargs = {"line"      : dict(width=self.pl_edge_width                ,
                                     color=self.pl_edge_color                ,
                                     shape=self.pl_edge_shape                ),
                  "mode"      : 'lines'                                      }
        self.pl_edges_lines = go.Scatter(**kwargs)
        edges    = self.nx_graph.edges()
        nodes    = self.nx_graph.nodes
        trace_xs = []
        trace_ys = []
        for edge in edges:
            x0, y0    = nodes[edge[0]]['pos']
            x1, y1    = nodes[edge[1]]['pos']
            trace_xs += [x0, x1, None]
            trace_ys += [y0, y1, None]
        self.pl_edges_lines['x'] = trace_xs
        self.pl_edges_lines['y'] = trace_ys
        return self


    def pl_create_edges_texts(self):
        texts  = []
        kwargs = {"mode"      : 'text'          }
        self.pl_edges_texts = go.Scatter(**kwargs)
        edges    = self.nx_graph.edges()
        nodes    = self.nx_graph.nodes
        trace_xs = []
        trace_ys = []
        for edge in edges:
            edge_data = edges[edge]
            x0, y0    = nodes[edge[0]]['pos']
            x1, y1    = nodes[edge[1]]['pos']
            texts.append(edge_data.get('text', '123'))
            trace_xs.append((x0+x1) / 2)
            trace_ys.append((y0+y1) / 2)
        self.pl_edges_texts['x'] = trace_xs
        self.pl_edges_texts['y'] = trace_ys
        self.pl_edges_texts['text'    ]          = texts
        self.pl_edges_texts['textfont']['color'] = self.pl_edge_text_color
        self.pl_edges_texts['textfont']['size' ] = self.pl_edge_text_size
        return self

    def pl_create_nodes(self):
        kwargs = {  "x"             : []                                          ,
                    "y"             : []                                          ,
                    "text"          : []                                          ,
                    "mode"          : self.pl_node_mode                           ,
                    "textposition"  : self.pl_node_text_position                  ,
                    "textfont"      : dict(color    = [] , size=[]               ),
                    "marker"        : dict(showscale= self.pl_node_show_scale    ,
                                           size     = self.pl_node_size          ,
                                           color    = self.pl_node_color         )}

        self.pl_nodes = go.Scatter(**kwargs)

        node_trace_xs = []
        node_trace_ys = []
        nodes = self.nx_graph.nodes()
        for node in nodes:
            print(nodes[node])
            x, y = self.nx_graph.nodes[node]['pos']
            node_trace_xs.append(x)
            node_trace_ys.append(y)
        self.pl_nodes['x'] = node_trace_xs
        self.pl_nodes['y'] = node_trace_ys
        return self

    def pl_set_node_traces_properties(self):
        colors = []
        texts  = []
        sizes  = []

        for node, adjacencies in enumerate(self.nx_graph.adjacency()):
            node_key   = adjacencies[0]
            node       = self.nx_graph.nodes[node_key]
            node_text  = node.get('value'    ) or node_key
            text_size  = node.get('text_size') or self.pl_node_text_size
            color      = node.get('color'    ) or 'blue'
            node_text  = node_text
            colors.append(color)
            texts .append(node_text)
            sizes .append(text_size)

        self.pl_nodes['text']              = texts
        self.pl_nodes['textfont']['color'] = colors
        self.pl_nodes['textfont']['size' ] = sizes
        return self

    def pl_figure_layout(self):
        kwargs = {  "title"      :  self.title                                                              ,
                    "titlefont"  :  dict(size=16)                                                           ,
                    "showlegend" :  self.pl_show_legend                                                     ,
                    "margin"     :  dict(b=21, l=5, r=5, t=40)                                              ,
                    "xaxis"      :  dict(showgrid=False, zeroline=False, showticklabels=False, mirror=True) ,
                    "yaxis"      :  dict(showgrid=False, zeroline=False, showticklabels=False, mirror=True) }

        return go.Layout(**kwargs)

    def create_plotly_figure(self):
        self.nx_create_positions_from_graph()
        self.assign_positions_to_graph()
        self.pl_create_edges_lines()
        self.pl_create_edges_texts()
        self.pl_create_nodes()
        self.pl_set_node_traces_properties()

        #
        kwargs =  { "data"  : [self.pl_edges_lines, self.pl_edges_texts, self.pl_nodes ],
                    "layout": self.pl_figure_layout()                                   }

        self.figure = go.Figure(**kwargs)
        return self


    def save_as_jpg(self, scale=1):
        if self.figure:
            image_bytes = self.figure.to_image(format='jpg', scale=scale)
            file_create_bytes(path=self.png_path, bytes=image_bytes)
        return self

    def set_graph(self, nx_graph):
        self.nx_graph = nx_graph
        return self

    def set_nx_spring_layout_k(self, value):
        self.nx_spring_layout_k = value
        return

    def set_title(self, title):
        self.title = title
        return self

    def create_png_from_nx_graph(self, nx_graph):
        self.set_graph(nx_graph)
        with Duration(prefix="create_plotly_figure: "):
            self.create_plotly_figure()
        with Duration(prefix="save_as_jpg:"):
            self.save_as_jpg()
        # (self.set_graph(graph)
        #      .create_plotly_figure()
        #      .save_as_jpg())
        return self


    # this will show the list of color scales: https://plotly.com/python/builtin-colorscales/
    #import plotly.express as px
    #self.figure = px.colors.sequential.swatches_continuous()