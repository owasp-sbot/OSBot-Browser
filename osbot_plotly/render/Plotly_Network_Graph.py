import math

import networkx
import plotly.graph_objects as go
##import networkx as nx
from osbot_linkedin.plotly.NX_Graph import NX_Graph
from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_create_bytes


class Plotly_Network_Graph:

    def __init__(self):
        self.figure                      = None
        self.nx_graph                    = networkx.Graph()
        self.jpg_scale                   = 1.0
        self.jpg_path                    = f"/tmp/plotly.jpg"
        self.title                       = 'Plotly Graph'
        self.nx_positions                = None
        self.nx_spring_layout_k          = 0.5                          # Optimal distance between nodes
        self.nx_spring_layout_iterations = 50                           # Maximum number of iterations taken
        self.nx_spring_layout_pos        = None                         # Initial positions for nodes as a dictionary with node as keys and values as a coordinate list or tuple.
        self.nx_spring_layout_fixed      = None                         # Nodes to keep fixed at initial position
        self.nx_spring_layout_center     = None                         # Coordinate pair around which to center the layout
        self.nx_spring_layout_scale      = 1                            # Scale factor for positions
        self.pl_edge_line_width          = 0.5
        self.pl_edge_line_color          = 'black'
        self.pl_edge_line_shape          = 'spline' #['linear', 'spline', 'hv', 'vh', 'hvh', 'vhv']
        self.pl_edge_text_color          = 'black'
        self.pl_edge_line_simplify       = True
        self.pl_edge_line_smoothing      = 1 # 0 and 1.3 - Has an effect only if `shape` is set to "spline" Sets the amount of smoothing
        self.pl_edge_text_size           = 7
        self.pl_node_text_size           = 6
        self.pl_node_text_color          = "black"
        self.pl_node_text_position       = "top center"
        self.pl_node_show_scale          = False
        self.pl_node_marker_size         = 6
        self.pl_node_marker_color        = "blue"
        self.pl_node_marker_symbol       = "circle"         # asterisk-open, arrow-up, bowtie, circle-open, circle-cross, cross, diamond, hash-open, hexagon, hourglass, line-ew-open, line-ns-open, square, square-cross, pentagon, star, star-diamond, triangle-left, x , y-left-open-  see list of available symbols here https://plotly.com/python/reference/scatter/#scatter-marker-symbol
        self.pl_show_legend              = False
        self.pl_edges_lines              = None
        self.pl_edges_texts              = None
        self.pl_nodes_texts              = None
        self.pl_nodes_markers            = None
        self.show_edges_arrows           = False
        self.show_edges_lines            = True
        self.show_edges_texts            = False
        self.show_nodes_markers          = True
        self.show_nodes_texts            = True
        self.on_add_node                 = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def nx_create_positions_from_graph(self):
        if self.nx_graph is not None:
            # see https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html
            kwargs = { "G"          : self.nx_graph                     ,   # NetworkX graph or list of nodes
                       "k"          : self.nx_spring_layout_k           ,   # Optimal distance between nodes
                       "pos"        : self.nx_spring_layout_pos         ,   # Initial positions for nodes as a dictionary with node as keys and values as a coordinate list or tuple.
                       "fixed"      : self.nx_spring_layout_fixed       ,   # Nodes to keep fixed at initial position
                       "iterations" : self.nx_spring_layout_iterations  ,   # Maximum number of iterations taken
                       "threshold"  : 1e-4                              ,   # Threshold for relative error in node position changes
                       "weight"     : "weight"                          ,   # The edge attribute that holds the numerical value used for the edge weight. Larger means a stronger attractive force
                       "scale"      : self.nx_spring_layout_scale       ,   # Scale factor for positions
                       "center"     : self.nx_spring_layout_center      ,   # Coordinate pair around which to center the layout
                       "dim"        : 2                                 ,   # Dimension of layout
                       "seed"       : 1                                 ,   # Set the random state for deterministic node layouts
                       }
            self.nx_positions = networkx.spring_layout(**kwargs)
        return self

    def assign_positions_to_graph(self):
        for n, p in self.nx_positions.items():
            self.nx_graph.nodes[n]['pos'] = p
        return self

    def pl_create_edges_lines(self):
        kwargs = {"line"      : dict(width     = self.pl_edge_line_width,
                                     color     = self.pl_edge_line_color,
                                     shape     = self.pl_edge_line_shape,
                                     simplify  = self.pl_edge_line_simplify,
                                     smoothing = self.pl_edge_line_smoothing),
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
        return self.pl_edges_lines

    def pl_create_edges_arrows(self):
        edges = self.nx_graph.edges()
        nodes = self.nx_graph.nodes

        for edge, edge_data in edges.items():
            edge_from_id = edge[0]
            edge_to_id   = edge[1]
            x0, y0    = nodes[edge_from_id]['pos']
            x1, y1    = nodes[edge_to_id  ]['pos']


            x0 = (x0 + x1) / 2          # this works quite effectively
            y0 = (y0 + y1) / 2          # which creates an arrow with the correct alignment (with half the size of the full line)
                                        # the code below was an attempt of creating a smaller arrow, which didn't work

            # angle = math.atan2(y1 - y0, x1 - x0)
            # pprint(angle)
            # length = 0.1
            #
            # x0 = x0 + length *  math.cos(angle)
            # y0 = y0 + length * math.sin(angle)

            annotation_kwargs = {
                "ax"         : x0     ,
                "ay"         : y0     ,
                "axref"      : 'x'    ,
                "ayref"      : 'y'    ,
                "x"          : x1     ,
                "y"          : y1     ,
                "xref"       : 'x'    ,
                "yref"       : 'y'    ,
                "showarrow"  : True   ,
                "arrowhead"  : 5      ,
                "arrowsize"  : 2      ,
                "arrowwidth" : self.pl_edge_line_width  ,
                "arrowcolor" : self.pl_edge_line_color  ,
                "standoff"   : 2      ,


            }
            self.figure.add_annotation(**annotation_kwargs)
        return self

    def pl_create_edges_texts(self):
        texts  = []
        kwargs = {"mode"      : 'text'          }
        self.pl_edges_texts = go.Scatter(**kwargs)
        edges    = self.nx_graph.edges()
        nodes    = self.nx_graph.nodes
        trace_xs = []
        trace_ys = []
        for edge, edge_data in edges.items():
            edge_from_id = edge[0]
            edge_to_id   = edge[1]
            edge_text    = edge_data.get('text', f'{edge_from_id} -> {edge_to_id}')
            x0, y0    = nodes[edge_from_id]['pos']
            x1, y1    = nodes[edge_to_id  ]['pos']
            trace_xs.append((x0+x1) / 2)
            trace_ys.append((y0+y1) / 2)
            texts.append(edge_text)

        self.pl_edges_texts['x'] = trace_xs
        self.pl_edges_texts['y'] = trace_ys
        self.pl_edges_texts['text'    ]          = texts
        self.pl_edges_texts['textfont']['color'] = self.pl_edge_text_color
        self.pl_edges_texts['textfont']['size' ] = self.pl_edge_text_size
        return self.pl_edges_texts

    def pl_create_nodes(self):
        if self.show_nodes_markers and self.show_nodes_texts:
            mode = 'text+markers'
        elif self.show_nodes_markers:
            mode = 'markers'
        else:
            mode = 'text'
        kwargs = {  "mode"          : mode                                    ,
                    #"textposition"  : self.pl_node_text_position              ,
                    "textfont"      : dict(color    = [] , size=[] )          ,
                    "marker"        : dict(showscale= self.pl_node_show_scale,
                                           size     = []                     ,
                                           color    = []                     ,
                                           symbol   = []                     )}

        self.pl_nodes_texts = go.Scatter(**kwargs)
        nx_nodes             = self.nx_graph.nodes()
        node_texts           = []
        node_texts_positions = []
        node_texts_xs        = []
        node_texts_ys        = []
        node_sizes           = []
        node_colors          = []
        marker_colors        = []
        marker_sizes         = []
        marker_symbols       = []

        #for nx_node in nx_nodes:
        for nx_node_id, nx_node_data in nx_nodes.items():
            #nx_node_data    = nx_nodes[nx_node]
            x, y            = nx_node_data.get('pos')

            node_add_args = { "x"                  : x                                                               ,
                              "y"                  : y                                                               ,
                              "nx_node_id"         : nx_node_id                                                      ,
                              "nx_node_data"       : nx_node_data                                                    ,
                              "node_text"          : nx_node_data.get('text'          , str(nx_node_id)            ) ,
                              "node_text_position" : nx_node_data.get('text_position' , self.pl_node_text_position) ,
                              "node_text_color"    : nx_node_data.get('text_color'    , self.pl_node_text_color    ) ,
                              "node_text_size"     : nx_node_data.get('text_size'     , self.pl_node_text_size     ) ,
                              "node_marker_color"  : nx_node_data.get('marker_color'  , self.pl_node_marker_color  ) ,
                              "node_marker_size"   : nx_node_data.get('marker_size'   , self.pl_node_marker_size   ) ,
                              "node_marker_symbol" : nx_node_data.get('marker_symbol' , self.pl_node_marker_symbol ) }

            if self.on_add_node:
                self.on_add_node(node_add_args)

            node_texts          .append(node_add_args.get('node_text'         ))
            node_texts_positions.append(node_add_args.get('node_text_position'))
            node_colors         .append(node_add_args.get('node_text_color'   ))
            node_sizes          .append(node_add_args.get('node_text_size'    ))
            node_texts_xs       .append(node_add_args.get('x'))
            node_texts_ys       .append(node_add_args.get('y'))
            marker_colors       .append(node_add_args.get('node_marker_color' ))
            marker_sizes        .append(node_add_args.get('node_marker_size'  ))
            marker_symbols      .append(node_add_args.get('node_marker_symbol'))


        self.pl_nodes_texts['x'       ]          = node_texts_xs
        self.pl_nodes_texts['y'       ]          = node_texts_ys
        self.pl_nodes_texts['text'    ]          = node_texts
        self.pl_nodes_texts['textfont']['color' ] = node_colors
        self.pl_nodes_texts['textfont']['size'  ] = node_sizes
        self.pl_nodes_texts['marker'  ]['color' ] = marker_colors
        self.pl_nodes_texts['marker'  ]['size'  ] = marker_sizes
        self.pl_nodes_texts['marker'  ]['symbol'] = marker_symbols
        self.pl_nodes_texts['textposition']       = node_texts_positions
        return self.pl_nodes_texts

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
        data = []
        if self.show_edges_lines:
            data.append(self.pl_create_edges_lines())

        if self.show_edges_texts:
            data.append(self.pl_create_edges_texts())

        if self.show_nodes_texts or self.show_nodes_markers:
            data.append(self.pl_create_nodes())
        #self.pl_set_node_traces_properties()

        #
        kwargs =  { "data"  : data                    ,
                    "layout": self.pl_figure_layout() }

        self.figure = go.Figure(**kwargs)

        if self.show_edges_arrows:               # arrows are added as annotations
            self.pl_create_edges_arrows()

        return self.figure


    def new_nx_graph(self):
        self.nx_graph = NX_Graph()#networkx.Graph()
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

    def set_nx_spring_layout_k(self, value):
        self.nx_spring_layout_k = value
        return

    def set_title(self, title):
        self.title = title
        return self

    def create_jpg_from_nx_graph(self, nx_graph=None):
        self.set_graph(nx_graph)
        with Duration(prefix=" >> create_plotly_figure: ", print_result=False):
            self.create_plotly_figure()
        with Duration(prefix=" >> save_as_jpg:", print_result=False):
           self.save_as_jpg()
        return self


    # this will show the list of color scales: https://plotly.com/python/builtin-colorscales/
    #import plotly.express as px
    #self.figure = px.colors.sequential.swatches_continuous()