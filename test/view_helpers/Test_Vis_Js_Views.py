from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda

from browser import Browser_Lamdba_Helper
from pbx_gs_python_utils.utils.Dev import Dev
from osbot_browser.view_helpers.Vis_Js_Views import Vis_Js_Views


class Test_Vis_Js_Views(TestCase):

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
        #graph_name = 'graph_EE3'    # fails in lamnda

        self.png_data = Vis_Js_Views.default(params=[graph_name])
        return

        browser_helper = Browser_Lamdba_Helper(headless=False).setup()
        pngData = browser_helper.get_screenshot_png(close_browser=False)
        browser_helper.save_png_data(pngData)

        #return



    def test_no_labels(self):
        self.png_data = Vis_Js_Views.no_labels(params=[self.graph_name])
        #self.png_data = Vis_Js_Views.no_labels(params=['aaaa__bbbb'])

    def test_node_label(self):
        self.graph_name = ['graph_VKN']
        label_key       = 'Summary'
        #label_key       = 'Issue Type'

        self.png_data = Vis_Js_Views.node_label(params=[self.graph_name, label_key])
        #Dev.pprint(self.png_data)

    def test_r1_r4(self):
        self.graph_name = 'graph_2Y4'
        self.png_data = Vis_Js_Views.r1_r4(params=[self.graph_name])
        Dev.pprint(self.png_data)
        #self.png_data = None

    def test_by_status(self):
        graph_name = 'graph_LGK' #'graph_9CP'#
        self.png_data = Vis_Js_Views.by_status(params=[graph_name])
        self.png_data = None

    def test_by_rating(self):
        self.png_data = Vis_Js_Views.by_rating(params=['graph_07B'])
        self.png_data = None

    def test_by_issue_type(self):
        # graph_RKR # large graph (r0 with 4 levels)
        graph_name = 'graph_9CP' #'graph_1Q5'  #
        self.png_data = Vis_Js_Views.by_issue_type(params=[graph_name],headless=False)
        #self.png_data = None

    def test_r1_pinned(self):
        # graph_RKR # large graph (r0 with 4 levels)
        graph_name = 'graph_S2H' #'graph_LGK' #'graph_1Q5'  #
        #graph_name ='graph_DAS'
        self.png_data = Vis_Js_Views.r1_pinned(params=[graph_name],headless=False)
        #self.png_data = None

    def test_hello_gs_cs(self):
        result = Vis_Js_Views.hello_gs_cs()
        result = Lambda('browser.lambda_browser').invoke({"params" : ["graph", "___","hello_gs_cs"]})
        Dev.pprint(result)



