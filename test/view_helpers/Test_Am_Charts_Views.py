from unittest import TestCase

from view_helpers.Am_Charts_Views import Am_Charts_Views
from browser import Browser_Lamdba_Helper
from pbx_gs_python_utils.utils.aws.Lambdas import Lambdas
from view_helpers.View_Examples import View_Examples


class Test_Am_Charts_Views(TestCase):

    def setUp(self):
        self.graph_name = 'graph_XKW'
        self.png_data   = None

    def tearDown(self):
        if self.png_data:
            Browser_Lamdba_Helper(headless=False).save_png_data(self.png_data)

    def test_default(self):
        graph_name = 'graph_XKW'    # (7 nodes)
        graph_name = 'graph_MKF'    # ( 20 nodes,  27 edges)
        #graph_name = 'graph_YT4'   # (199 nodes, 236 edges)
        #graph_name = 'graph_VZ5'   # (367 nodes, 653 edges)
        #graph_name = 'graph_EE3'    # fails in lambda in visjs (but works here :) )
        #graph_name = 'graph_OJF'   # org chart
        self.png_data = Am_Charts_Views.default(params=[graph_name],headless=False)

    def test_chord   (self): self.png_data = Am_Charts_Views.chord   (params=['graph_MKF'], headless=False)
    def test_triangle(self): self.png_data = Am_Charts_Views.triangle(params=[           ], headless=False)

    def test_open_file_in_browser__am_charts(self):
        #View_Examples(headless=False).open_file_in_browser('/go-js/sankey.html')
        View_Examples(headless=False).open_file_in_browser('/am_charts/triangle.html')


    def test_update_lambda(self):
        Lambdas('browser.lambda_browser').update_with_src()