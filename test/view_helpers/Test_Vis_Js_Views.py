from unittest import TestCase

from browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from utils.Dev import Dev
from utils.aws.Lambdas import Lambdas
from view_helpers.Vis_Js_Views import Vis_Js_Views


class Test_Vis_Js_Views(TestCase):

    def setUp(self):
        self.graph_name = 'graph_XKW'
        self.png_data   = None

    def tearDown(self):
        if self.png_data:
            Browser_Lamdba_Helper().save_png_data(self.png_data)

    def test_default(self):
        graph_name = 'graph_XKW'    # (7 nodes)
        #graph_name = 'graph_MKF'    # ( 20 nodes,  27 edges)
        #graph_name = 'graph_YT4'   # (199 nodes, 236 edges)
        #graph_name = 'graph_VZ5'   # (367 nodes, 653 edges)
        self.png_data = Vis_Js_Views.default(params=[graph_name])


    def test_no_labels(self):
        self.png_data = Vis_Js_Views.no_labels(params=[self.graph_name])
        #self.png_data = Vis_Js_Views.no_labels(params=['aaaa__bbbb'])

    def test_node_label(self):
        self.graph_name = ['graph_VKN']
        label_key       = 'Summary'
        #label_key       = 'Issue Type'

        self.png_data = Vis_Js_Views.node_label(params=[self.graph_name, label_key])
        #Dev.pprint(self.png_data)

    def test_r0_r1_r2(self):
        self.graph_name = 'graph_YXF'
        self.png_data = Vis_Js_Views.r0_r1_r2(params=[self.graph_name])
        #Dev.pprint(self.png_data)
        self.png_data = None

    def test_by_status(self):
        self.png_data = Vis_Js_Views.by_status(params=['graph_YXF'])
        self.png_data = None

    def test_update_lambda(self):
        Lambdas('browser.lambda_browser').update_with_src()


