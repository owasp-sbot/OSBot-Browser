from unittest import TestCase

from browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from utils.Dev import Dev
from view_helpers.Vis_Js_Views import Vis_Js_Views


class Test_Vis_Js_Views(TestCase):

    #def setUp(self):
    #    self

    def test_default(self):
        graph_name = 'graph_MKF'  # ( 20 nodes,  27 edges)
        graph_name = 'graph_YT4'  # (199 nodes, 236 edges)
        #graph_name = 'graph_VZ5'
        params = [graph_name]
        png_data = Vis_Js_Views.default(params=params)
        #Dev.pprint(png_data)
        Browser_Lamdba_Helper().save_png_data(png_data)

