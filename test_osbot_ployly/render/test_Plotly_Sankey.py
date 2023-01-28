from unittest import TestCase
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from osbot_plotly.render.Plotly_Sankey import Plotly_Sankey
from osbot_utils.utils.Dev import pprint


class test_Plotly_Sankey(TestCase):

    def setUp(self):
        self.plotly_sankey = Plotly_Sankey()

    def create_test_graph(self):
        df = px.data.wind()
        return nx.from_pandas_edgelist(df, source="strength", target="frequency")  # , edge_attr='frequency')

    def test_mvp(self):
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                label=[{"text": "A", "font": {"size": 20}},
                       {"text": "B", "font": {"size": 20}},
                       {"text": "C", "font": {"size": 20}}],
                color="blue"
            ),
            link=dict(
                source=[0, 1, 0],  # indices correspond to labels
                target=[2, 2, 1],
                value=[8, 4, 2]
            )
        )])
        self.plotly_sankey.set_figure(fig)
        self.plotly_sankey.save_as_jpg()

    def test_networkx(self):
        import networkx as nx
        import plotly.graph_objects as go

        # G = nx.DiGraph()
        # G.add_nodes_from(['A', 'B', 'C', 'D', 'E'])
        # G.add_edges_from([('A', 'B'), ('C', 'D'),
        #                     ('A', 'C'), ('C', 'B') ,
        #                   ('A', 'E')])

        nx_graph = self.create_test_graph()
        self.plotly_sankey.create_from_nx_graph(nx_graph)
        #self.plotly_sankey.set_figure(fig)
        self.plotly_sankey.save_as_jpg()