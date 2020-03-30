from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.api.API_Image import API_Image
from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_browser.view_helpers.VivaGraph_Js import VivaGraph_Js
from osbot_jira.api.graph.GS_Graph import GS_Graph
from osbot_jira.api.graph.Lambda_Graph import Lambda_Graph


class Test_VivaGraph_Js(Test_Helper):

    def setUp(self):
        super().setUp()
        self.vivagraph_js = VivaGraph_Js(headless=False)
        #self.result    = None

    #def tearDown(self):
    #    if self.result is not None:
    #        Dev.pprint(self.result)

    def test_create_graph(self):
        (nodes, edges, graph_data, graph_name) = (0,0,0,None)
        Dev.pprint(self.vivagraph_js.create_graph(nodes, edges))

    def test_create_graph_and_send_screenshot_to_slack(self):
        nodes = [{'key': 'TEAM-23', 'label': 'TEAM-23', 'img_url': 'icons/TEAM.png', 'img_size': 20}]
        edges = []
        png_data = self.vivagraph_js.create_graph_and_send_screenshot_to_slack(nodes, edges)
        image = (API_Image().load_from_bytes_base64(png_data)
                            .set_img_file('/tmp/temp_image.png')
                            .save())

        # import base64
        # from PIL import Image
        # import io
        self.result = image.info()
        # #self.result = 'asd'

    def test_vis_js(self):
        graph_name = 'graph_I3H'
        #graph_name = 'graph_N59'   # raw data
        #graph_name = 'graph_BP9'    # created graph
        
        from osbot_browser.view_helpers.Vis_Js_Views import Vis_Js_Views
        self.png_data = Vis_Js_Views.default(params=[graph_name],headless=False)

        
    def test_get_graph_data(self):

        graph_name = 'graph_I3H'
        #graph_name = 'graph_782' #
        graph_name = 'graph_N59'

        source_graph_data =  Lambda_Graph().get_graph_data(graph_name)
        root_key = 'Issues Created'
        gs_graph = GS_Graph()
        gs_graph.add_node(root_key)

        for key, node in source_graph_data['nodes'].items():
            if node is None:
                continue
            creator    = node.get('Creator')
            issue_type = node.get('Issue Type')

            issue_type_key = f'{issue_type}-{creator}'

            gs_graph.add_node(key)
            gs_graph.add_node(creator)
            gs_graph.add_node(issue_type_key)

            gs_graph.add_edge(root_key       , '..', creator       )
            gs_graph.add_edge(creator        , '..', issue_type_key)
            gs_graph.add_edge(issue_type_key , '..', key           )


        self.result =  Lambda_Graph().save_gs_graph(gs_graph)
        #self.result = gs_graph.get_graph_data()

        #self.vivagraph_js.render_wait = 2
        #self.png_data = self.vivagraph_js.render_gs_graph(gs_graph)








    # todo: refactor out into new class
    def test_save_jira_icons_locally(self):
        self.result = self.vivagraph_js.save_jira_icons_locally()


