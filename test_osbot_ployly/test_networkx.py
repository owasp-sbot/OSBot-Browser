from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_create_bytes


class test_networkx(TestCase):

    def save_png(self, fig):
        format = 'jpg'
        scale = 1
        image_bytes = fig.to_image(format=format, scale=scale)
        png_path = f"/tmp/plotly.{format}"
        file_create_bytes(path=png_path, bytes=image_bytes)


    def test_create_graph(self):
        import plotly.graph_objects as go

        import networkx as nx

        G = nx.random_geometric_graph(200, 0.125)

        # create edges

        edge_x = []
        edge_y = []

        for edge in G.edges():
            x0, y0 = G.nodes[edge[0]]['pos']
            x1, y1 = G.nodes[edge[1]]['pos']
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        for node in G.nodes():
            x, y = G.nodes[node]['pos']
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                # colorscale options
                # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))

        # color node points

        node_adjacencies = []
        node_text = []
        for node, adjacencies in enumerate(G.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            node_text.append('# of connections: ' + str(len(adjacencies[1])))

        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text


        # create network graph

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='<br>Network graph made with Python',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=[dict(
                                text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002)],
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )

        self.save_png(fig)


    def test_df_graph(self):
        import plotly.express as px
        import networkx as nx
        df = px.data.wind()
        G = nx.from_pandas_edgelist(df,source="direction", target="strength", edge_attr='frequency')
        #nx.draw(G)


    def test_df_graph_2(self):
        import random
        node_list = ["A", "B", "C", "D", "E", "F", "G", "H", "E"]

        def draw_number(length):
            """determines a random index number for selection."""
            from_index = random.randint(0, length)
            to_index = random.randint(0, length)
            return from_index, to_index

        from_list = []
        to_list = []
        counter = 20
        i = 0
        while i < counter:
            from_index, to_index = draw_number(len(node_list) - 1)
            if from_index == to_index:
                continue
            from_list.append(node_list[from_index])
            to_list.append(node_list[to_index])
            i += 1

        import networkx as nx
        import plotly.graph_objs as go
        G = nx.Graph()
        for i in range(len(node_list)):
            G.add_node(node_list[i])
            G.add_edges_from([(from_list[i], to_list[i])])

        import plotly.express as px
        df = px.data.wind()
        G = nx.from_pandas_edgelist(df, source="strength", target="frequency")#, edge_attr='frequency')


        self.save_png(fig)