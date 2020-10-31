from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from osbot_browser.view_helpers.Vis_Js_Views import Vis_Js_Views


class Test_Vis_Js_Views(Test_Helper):

    def setUp(self):
        super().setUp()
        self.graph_name = 'graph_BMM'
        self.png_data   = None

    def tearDown(self):
        if self.png_data:
            Browser_Lamdba_Helper(headless=False).save_png_data(self.png_data)



    def test_default(self):
        graph_name = 'graph_X3X' # 'graph_JF4'
        self.png_data = Vis_Js_Views.default(params=[graph_name],headless=False)




    def test_no_labels(self):
        self.png_data = Vis_Js_Views.no_labels(params=[self.graph_name])
        #self.png_data = Vis_Js_Views.no_labels(params=['aaaa__bbbb'])

    def test_node_label(self):
        self.graph_name = ['graph_J2O']
        label_key       = 'Summary'
        self.result = Vis_Js_Views.node_label(params=[self.graph_name, label_key], headless=False)
        #Dev.pprint(self.png_data)

    def test_r1_r4(self):
        self.graph_name = 'graph_2Y4'
        self.png_data = Vis_Js_Views.r1_r4(params=[self.graph_name])
        #self.png_data = None

    def test_by_status(self):
        graph_name = 'graph_TAP' #'graph_9CP'#
        self.png_data = Vis_Js_Views.by_status(params=[graph_name],headless=False)
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



