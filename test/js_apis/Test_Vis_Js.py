import base64
import json
from unittest import TestCase

from browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from src.js_apis.Vis_Js import Vis_Js
from utils.Assert import Assert
from utils.Dev import Dev
from utils.Misc import Misc


class Test_Vis_Js(TestCase):
    def setUp(self):
        self.vis_js  = Vis_Js()#.setup()
        self.browser = self.vis_js.browser()

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
        Assert(self.vis_js.web_root                ).contains   ('serverless-render/src/web_root'       )
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
        self.vis_js.load_page(True)
        nodes   = [{'id':'123','label': 'aaaa','x':-20 ,'fixed': {'x': True,'y':True}},
                   {'id':'aaa','label': '123' , 'x':200,'fixed': {'x': True}}]
        edges   = [{'from':'123','to' :'aaa'}]
        options = {}
        self.vis_js.create_graph(nodes, edges, options)

        #
        #base64_data = base64.b64encode(json.dumps(data).encode()).decode()
        #base64_options = base64.b64encode(json.dumps(options).encode()).decode()
        #js_code = "window.network = new vis.Network(container, JSON.parse(atob('{0}')), JSON.parse(atob('{1}')));".format(base64_data,base64_options)
        #self.vis_js.exec_js(js_code)
        #Dev.print(js_code)

    def test_get_graph_data(self):
        graph_name = 'graph_MKF'
        graph_name = 'graph_YT4'
        result = self.vis_js.get_graph_data(graph_name)
        Dev.print(result)

    def test_show_jira_graph(self):
        label_key = 'Issue Type'
        label_key = 'Summary'
        #graph_name = 'graph_MKF'
        graph_name = 'graph_YT4'
        result = self.vis_js.show_jira_graph(graph_name, label_key=label_key)
        #result = self.vis_js.send_screenshot_to_slack(None, None)
        #Dev.print(result)



