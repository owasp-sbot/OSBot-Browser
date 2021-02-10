import json
from unittest import TestCase

from osbot_utils.utils.Dev import Dev

from osbot_browser.Deploy import Deploy
from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from osbot_browser.view_helpers.Am_Charts_Views import Am_Charts_Views
from osbot_browser.view_helpers.View_Examples import View_Examples


class Test_Am_Charts_Views(TestCase):

    def setUp(self):
        self.graph_name = 'graph_XKW'
        self.png_data   = None
        self.result     = None

    def tearDown(self):
        if self.png_data:
            Browser_Lamdba_Helper(headless=False).save_png_data(self.png_data)
        if self.result:
            Dev.pprint(self.result)

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

    def test_timeline(self):
        data = [{"x": "1","y": 1,"text": "[bold]2018 Q1[/]\nThere seems to be some furry animal living in the neighborhood.", "center": "bottom"}, {
                  "x": "2",
                  "y": 1,
                  "text": "[bold]2018 Q2[/]\nWe're now mostly certain it's a fox.",
                  "center": "top"
                }, {
                  "x": "3",
                  "y": 1,
                  "text": "[bold]2018 Q3[/]\nOur dog does not seem to mind the newcomer at all.",
                  "center": "bottom"
                }, {
                  "x": "4",
                  "y": 1,
                  "text": "[bold]2018 Q4[/]\nThe quick brown fox jumps over the lazy dog.",
                  "center": "top"
                }];
        params = json.dumps(data).split(' ')
            #['SEC-11911'] # timeline
        #self.png_data = Am_Charts_Views.timeline(params=params, headless=False)
        self.result = Am_Charts_Views.timeline(params=params, headless=False)




    def test_open_file_in_browser__am_charts(self):
        #View_Examples(headless=False).open_file_in_browser('/go-js/sankey.html')
        View_Examples(headless=False).open_file_in_browser('/am_charts/main.html')


    def test_deploy_lambda_function(self):

        Deploy('osbot_browser.lambdas.lambda_browser').deploy()