import json
from unittest import TestCase

from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from osbot_browser.view_helpers.Vis_Js import Vis_Js
from osbot_utils.utils.Assert import Assert
from osbot_utils.utils.Dev import Dev


class Test_Vis_Js(Test_Helper):
    def setUp(self):
        super().setUp()
        self.headless = False
        self.vis_js   = Vis_Js(self.headless)
        self.browser  = self.vis_js.browser()

    def tearDown(self):
        png_data = self.browser.sync__screenshot_base64()
        Browser_Lamdba_Helper().save_png_data(png_data)


    def test_add_node(self):
        (
            self.vis_js.add_node('1','first node')
                       .add_node('2', '2nd node')
                       .add_edge('1','2')
        )

    def test_add_node__100_nodes(self):
        colors = ['#9999FF','lightred','lightgreen']
        js_codes = []
        js_codes.append(self.vis_js.add_node__js_code('root', 'root_node','box'))

        for i in range(0,100):
            color = colors[i % 3]
            js_codes.append(self.vis_js.add_node__js_code(i,i, color=color))
            js_codes.append(self.vis_js.add_edge__js_code('root', i))

        self.vis_js.exec_js(js_codes)

    #def test_set_nodes

    def test_setup(self):
        Assert(self.browser                        ).is_class   ('API_Browser'                          )
        Assert(self.vis_js.web_root                ).contains   ('serverless-render/osbot_browser/web_root'       )
        Assert(self.browser.sync__url()            ).is_equal   ('about:blank')
        Dev.print(self.browser.sync__url())
        #Assert(self.browser.sync__url()            ).match_regex('http://localhost:.*/vis-js/empty.html')

    def test_exec_js(self):
        self.vis_js.load_page(True)
        js_code = """
                network.body.data.nodes.add({id:'1',label:'1st node..'})
                network.body.data.nodes.add({id:'12',label:'new node'})
                network.body.data.edges.add({from:'12',to:'1'})
                """
        self.vis_js.exec_js(js_code)

    def test_create_graph(self):
        nodes   = [{'id':'123','label': 'aaaa','x':-20 ,'fixed': {'x': True,'y':True}},
                   {'id':'aaa','label': '123' , 'x':200,'fixed': {'x': True}}]
        edges   = [{'from':'123','to' :'aaa'}]
        options = {}
        self.vis_js.create_graph(nodes, edges, options)



    def test_get_graph_data(self):
        graph_name = 'graph_MKF'             # small          ( 20 nodes,  27 edges)
        #graph_name = 'graph_YT4'            # large one      (199 nodes, 236 edges)
        #graph_name = 'graph_VZ5'            # very large one (367 nodes, 653 edges)
        result = self.vis_js.get_graph_data(graph_name)
        Dev.pprint("{0} nodes, {1} edges".format(len(result.get('nodes')), len(result.get('edges'))))

    def test_show_jira_graph(self):
        label_key = 'Issue Type'
        label_key = 'Summary'
        graph_name = 'graph_MKF'
        #graph_name = 'graph_YT4'
        #graph_name = 'graph_XKW'
        result = self.vis_js.show_jira_graph(graph_name, label_key=label_key)
        #result = self.vis_js.send_screenshot_to_slack(None, None)
        Dev.print(result)





