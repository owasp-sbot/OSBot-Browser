import plotly.graph_objects as go
import networkx as nx

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_create_bytes


class Plotly_Network_Graph:

    def __init__(self):
        self.figure          = None
        self.graph           = None
        self.png_path        = f"/tmp/plotly.jpg"
        self.title           = 'Plotly Graph'
        self.spring_layout_k = 1.00

    def create_plotly_figure(self):
        pos = nx.spring_layout(self.graph, k=self.spring_layout_k, iterations=500)
        #pos = nx.circular_layout(self.graph)
        for n, p in pos.items():
            self.graph.nodes[n]['pos'] = p

        #edge_trace
        edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=0.5, color='#888',shape='spline'),
            hoverinfo='none',
            mode='lines')
        for edge in self.graph.edges():
            x0, y0 = self.graph.nodes[edge[0]]['pos']
            x1, y1 = self.graph.nodes[edge[1]]['pos']
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])


        # node trace
        node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers+text',
            #mode='text',
            #hoverinfo='text',
            textposition="top center",
            textfont=dict(color=[], size=[]),
            marker=dict(showscale=False,
                        size=6,
                       #colorscale='blues',
                        #reversescale=True,
                        color='gray'
                        #size=37,
                        ))
        for node in self.graph.nodes():
            x, y = self.graph.nodes[node]['pos']
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])

        for node, adjacencies in enumerate(self.graph.adjacency()):
            node_key   = adjacencies[0]
            node       = self.graph.nodes[node_key]
            node_text  = node.get('value')
            text_size  = node.get('text_size')
            color      = node.get('color'    )

            #print(adjacencies)
            #node_trace['marker']['color'] += tuple([len(adjacencies[1])])
            #marker = node_trace['marker']
            #marker['size'] = 10
            #fillpattern
            #node_trace['marker']['color'] = 'white'
            #node_trace['marker']['symbol'] = 'square'
            node_trace['textfont']['color'] += tuple([color])
            node_trace['textfont']['size'] += tuple([text_size])

            node_text = node_text
            node_trace['text'] += tuple([node_text])



        #add the figure
        #title = "Network Graph Demonstration"
        self.figure = go.Figure(data=[edge_trace, node_trace],
                                layout=go.Layout(title=self.title,
                                                 titlefont=dict(size=16),
                                                 showlegend=False,
                                                 hovermode='closest',
                                                 margin=dict(b=21, l=5, r=5, t=40),
                                                 # annotations=[dict(
                                                 #    text="Text Here!!!!",
                                                 #    showarrow=False,
                                                 #    xref="paper", yref="paper")],
                                                xaxis=dict(showgrid=False, zeroline=False,
                                                           showticklabels=False, mirror=True),
                                                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, mirror=True)))
        return self

    def save_as_jpg(self, scale=2):
        image_bytes = self.figure.to_image(format='jpg', scale=scale)
        file_create_bytes(path=self.png_path, bytes=image_bytes)
        return self

    def set_graph(self, graph):
        self.graph = graph
        return self

    def set_spring_layout_k(self, value):
        self.spring_layout_k = value
        return

    def set_title(self, title):
        self.title = title
        return self

    def create_png_from_graph(self, graph):
        (self.set_graph(graph)
             .create_plotly_figure()
             .save_as_jpg())
        return self


    # this will show the list of color scales: https://plotly.com/python/builtin-colorscales/
    #import plotly.express as px
    #self.figure = px.colors.sequential.swatches_continuous()