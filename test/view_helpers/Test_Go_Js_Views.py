from unittest import TestCase

from view_helpers.Go_Js_Views import Go_Js_Views
from browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from utils.Dev import Dev
from utils.aws.Lambdas import Lambdas
from view_helpers.View_Examples import View_Examples


class Test_Go_Js_Views(TestCase):

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
        self.png_data = Go_Js_Views.default(params=[graph_name])


    def test_circular (self): self.png_data = Go_Js_Views.circular (params=['graph_GYY'])
    def test_sankey   (self): self.png_data = Go_Js_Views.sankey   (params=['graph_MKF'])
    def test_swimlanes(self): self.png_data = Go_Js_Views.swimlanes(params=['graph_MKF'])
    def test_mindmap  (self): self.png_data = Go_Js_Views.mindmap  (params=['graph_FCM'])
    def test_piechart (self): self.png_data = Go_Js_Views.piechart (params=['_'        ])
    def test_kanban   (self): self.png_data = Go_Js_Views.kanban   (params=['graph_MKF'],headless=False)
    def test_timeline (self): self.png_data = Go_Js_Views.timeline (params=['graph_MKF'],headless=False)

    def test_chart_js(self): self.png_data = Go_Js_Views.chart_js(params=['_'])

    def test_mindmap___with_size(self):
        self.png_data = Go_Js_Views.mindmap(params=['graph_EPU',1000,300])

    def test_mindmap___with_non_issue_nodes(self):
        self.png_data = Go_Js_Views.mindmap(params=['graph_THV',1000,500])

    def test_mindmap_issue(self):
        import json
        jira_id = 'GSCS-14'
        #jira_id = 'IA-402'
        self.png_data = Go_Js_Views.mindmap_issue(params=[jira_id])
        #params = [graph_name]


    def test_open_file_in_browser__go_gs(self):
        #View_Examples(headless=False).open_file_in_browser('/go-js/sankey.html')
        View_Examples(headless=False).open_file_in_browser('/go-js/mindmap.html')

    def test_open_file_in_browser__am_charts(self):
        #View_Examples(headless=False).open_file_in_browser('/go-js/sankey.html')
        View_Examples(headless=False).open_file_in_browser('/am_charts/triangle.html')

    # bugs

    def test_fixed__bug_default_doesnt_render(self):
        self.png_data = Go_Js_Views.default(params=['graph_414']) # graph_name has a node whose text is None

    def test_fixed__bug_cache_issue_in_lambdas(self):
        Lambdas('browser.lambda_browser').update_with_src()

        payload = { "params" : ["go_js","graph_MKF", "default"]}
        self.png_data = Lambdas('browser.lambda_browser').invoke(payload)
        Dev.pprint(self.png_data)

        self.png_data = Lambdas('browser.lambda_browser').invoke(payload)
        Dev.pprint(self.png_data)

    def test_fixed__bug___graph_breaks_mindmap(self):
        #graph_name = 'graph_W2E'  # example 1
        graph_name = 'graph_0QZ'   # example 2
        self.png_data = Go_Js_Views.mindmap(params=[graph_name])

    def test_fixed_bug___graph_doesnt_create_good_mindmap(self):
        graph_name = 'graph_56Q'    # prob was this graph (that was missing a root node)
        graph_name = 'graph_O80'
        self.png_data = Go_Js_Views.mindmap(params=[graph_name])


    # update lambda
    def test_update_lambda(self):
        Lambdas('browser.lambda_browser').update_with_src()
