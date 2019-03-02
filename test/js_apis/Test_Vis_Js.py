from unittest import TestCase

from browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from src.js_apis.Vis_Js import Vis_Js
from utils.Assert import Assert
from utils.Dev import Dev
from utils.Misc import Misc


class Test_Vis_Js(TestCase):
    def setUp(self):
        self.vis_js  = Vis_Js().setup()
        self.browser = self.vis_js.browser

    def tearDown(self):
        png_data = self.browser.get_screenshot_png()
        self.browser.save_png_data(png_data)


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

        for i in range(0,50):
            color = colors[i % 3]
            js_codes.append(self.vis_js.add_node__js_code(i,i, color=color))
            js_codes.append(self.vis_js.add_edge__js_code('root', i))

        self.vis_js.exec_js(js_codes)

    #def test_set_nodes

    def test_setup(self):
        Assert(self.browser                        ).is_class   ('Browser_Lamdba_Helper'                )
        Assert(self.browser.web_root()             ).contains   ('serverless-render/src/web_root'       )
        Assert(self.browser.api_browser.sync__url()).match_regex('http://localhost:.*/vis-js/empty.html')

    def test_exec_js(self):
        js_code = """
                network.body.data.nodes.add({id:'1',label:'1st node'})
                network.body.data.nodes.add({id:'12',label:'new node'})
                network.body.data.edges.add({from:'12',to:'1'})
                """
        self.vis_js.exec_js(js_code)


