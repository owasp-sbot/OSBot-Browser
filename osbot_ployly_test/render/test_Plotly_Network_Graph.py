from unittest import TestCase
import plotly.express as px
import networkx as nx
from osbot_plotly.render.Plotly_Network_Graph import Plotly_Network_Graph
from osbot_utils.utils.Dev import pprint


class test_Plotly_Network_Graph(TestCase):

    def setUp(self) -> None:
        self.network_graph = Plotly_Network_Graph()

    def test_graph(self):
        df = px.data.wind()
        return nx.from_pandas_edgelist(df, source="strength", target="frequency")  # , edge_attr='frequency')

    def test_create_jpg_from_test_graph(self):
        graph = self.test_graph()
        self.network_graph.set_graph(graph)
        self.network_graph.create_plotly_figure()
        self.network_graph.save_as_jpg()

    def test_create_jpg_from_manual_graph(self):
        graph = nx.Graph()
        graph.add_nodes_from([1,2,3,4,5,6,7,"ABC"])
        graph.add_edges_from([(1,2), (1,3), (1,4), (2,3)])
        self.network_graph.create_png_from_nx_graph(graph)




