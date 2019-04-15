from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev
from osbot_browser.view_helpers.VivaGraph_Js import VivaGraph_Js


class Test_VivaGraph_Js(TestCase):

    def setUp(self):
        self.vivagraph = VivaGraph_Js()

    def test_create_graph(self):
        (nodes, edges, graph_data, graph_name) = (0,0,0,None)
        Dev.pprint(self.vivagraph.create_graph(nodes, edges, graph_data, graph_name))


