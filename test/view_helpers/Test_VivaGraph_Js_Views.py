from unittest import TestCase

from gw_bot.Deploy import Deploy
from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from osbot_browser.view_helpers.VivaGraph_Js_Views import VivaGraph_Js_Views


class Test_VivaGraph_Js_Views(Test_Helper):

    def setUp(self):
        super().setUp()
        self.graph_name = 'graph_XKW'
        self.png_data   = None

    # def tearDown(self):
    #     super().defau
    #     if self.png_data:
    #         Browser_Lamdba_Helper().save_png_data(self.png_data)



    def test_deploy_lambda_function(self):
        self.result = Deploy().deploy_lambda__browser()

    def test_default(self):
        #graph_name = 'graph_I3H' #'graph_UUZ'
        graph_name = 'graph_24O'
        #graph_name = 'graph_041'  # large one  (doesn't work headless)
        channel    = None #'CSK9RADE2'
        headless   = True
        screenshot = True
        self.png_data = VivaGraph_Js_Views.default(params=[graph_name], screenshot=screenshot, headless=headless, channel=channel)
        #self.png_data = False

    def test_default__check_width(self):
        graph_name    = 'graph_03K'
        browser_width = 200
        render_wait   = 0
        screenshot    = False
        vivagraph_js = VivaGraph_Js_Views.default(params=[graph_name,browser_width, render_wait], screenshot=screenshot)
        assert vivagraph_js.browser_width == browser_width
        assert  vivagraph_js.render_wait == render_wait


    def test_default__with_non_issue_nodes(self):
        graph_name = 'graph_THV'                    # create by an group_by filter
        self.png_data = VivaGraph_Js_Views.default(params=[graph_name])


    def test_by_no_key(self):
        graph_name = 'graph_24O'    # ( 20 nodes,  27 edges)
        #graph_name = 'graph_041'
        self.png_data = VivaGraph_Js_Views.no_key(params=[graph_name],headless=True)

    def test_by_node_value(self):
        graph_name = 'graph_UUZ'
        field      = 'Status'
        self.png_data = VivaGraph_Js_Views.node_value(params=[graph_name,field],headless=False)
        #self.png_data = False

    # def test_people(self):
    #     graph_name = 'graph_CR9'
    #     self.png_data = VivaGraph_Js_Views.people(params=[graph_name],headless=True)

    # bugs

    def test_fixed__bug_graph_doesnt_render(self):
        graph_name = 'graph_AEY'
        graph_name = 'graph_NP5'
        self.png_data = VivaGraph_Js_Views.default(params=[graph_name],headless=True)

    def test_fixed_bug__broken_images(self):
        graph_name = 'graph_34F'
        self.png_data = VivaGraph_Js_Views.default(params=[graph_name],headless=False)


