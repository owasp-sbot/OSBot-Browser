from unittest import TestCase

from browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from utils.Dev import Dev
from utils.aws.Lambdas import Lambdas
from view_helpers.VivaGraph_Js_Views import VivaGraph_Js_Views


class Test_VivaGraph_Js_Views(TestCase):

    def setUp(self):
        self.graph_name = 'graph_XKW'
        self.png_data   = None

    def tearDown(self):
        if self.png_data:
            Browser_Lamdba_Helper(headless=False).save_png_data(self.png_data)

    def test_default(self):
        graph_name = 'graph_XKW'    # (7 nodes)
        graph_name = 'graph_MKF'    # ( 20 nodes,  27 edges)
        graph_name = 'graph_YT4'   # (199 nodes, 236 edges)
        #graph_name = 'graph_VZ5'   # (367 nodes, 653 edges)
        #graph_name = 'graph_EE3'    # fails in lambda in visjs (but works here :) )
        self.png_data = VivaGraph_Js_Views.default(params=[graph_name])
        self.png_data = False

        #return

    def test_by_issue_type(self):
        graph_name = 'graph_XKW'    # (7 nodes)
        graph_name = 'graph_MKF'    # ( 20 nodes,  27 edges)

        self.png_data = VivaGraph_Js_Views.by_issue_type(params=[graph_name])
        self.png_data = False

    def test_by_field(self):
        graph_name = 'graph_XKW'    # (7 nodes)
        graph_name = 'graph_MKF'    # ( 20 nodes,  27 edges)
        field      = 'Labels' # ''Rating'
        self.png_data = VivaGraph_Js_Views.by_field(params=[graph_name,field])
        self.png_data = False








    def test_update_lambda(self):
        Lambdas('browser.lambda_browser').update_with_src()


