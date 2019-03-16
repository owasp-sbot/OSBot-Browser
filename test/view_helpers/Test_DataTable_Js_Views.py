from unittest import TestCase

from browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from utils.Dev import Dev
from utils.aws.Lambdas import Lambdas
from view_helpers.DataTable_Js_Views import DataTable_Js_Views


class Test_DataTable_Js_Views(TestCase):

    def setUp(self):
        self.graph_name = 'graph_XKW'
        self.png_data   = None

    def tearDown(self):
        Browser_Lamdba_Helper().save_png_data(self.png_data)

    def test_graph(self):
        graph_name = 'graph_XKW'    # (7 nodes)
        graph_name = 'graph_MKF'    # ( 20 nodes,  27 edges)
        #graph_name = 'graph_YT4'   # (199 nodes, 236 edges)
        #graph_name = 'graph_VZ5'   # (367 nodes, 653 edges)
        graph_name  = 'graph_W4T'   # R1 Labels (from search results)
        graph_name = 'graph_9CP'
        self.png_data = DataTable_Js_Views.graph(params=[graph_name])

    def test_graph_simple(self):
        graph_name = 'graph_9CP'
        self.png_data = DataTable_Js_Views.graph_simple(params=[graph_name])
        Dev.pprint(self.png_data)

    def test_graph_all_fields(self):
        graph_name = 'graph_XKW'    # (7 nodes)
        #graph_name = 'graph_MKF'    # ( 20 nodes,  27 edges)
        #graph_name = 'graph_YT4'   # (199 nodes, 236 edges)
        #graph_name = 'graph_VZ5'   # (367 nodes, 653 edges)
        self.png_data = DataTable_Js_Views.graph_all_fields(params=[graph_name])

    def graph_all_fields__issue_id(self):
        graph_name = 'GSSP-111'
        self.png_data = DataTable_Js_Views.graph_all_fields(params=[graph_name])

    def test_issue(self):
        issue_id = 'GSSP-111'
        self.png_data = DataTable_Js_Views.issue(params=[issue_id])


    def test_test_data(self):
        self.png_data = DataTable_Js_Views.test_data()

    def test_update_lambda(self):
        Lambdas('browser.lambda_browser').update_with_src()


