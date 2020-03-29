from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from gw_bot.api.API_Image import API_Image
from gw_bot.helpers.Test_Helper import Test_Helper
from osbot_browser.view_helpers.VivaGraph_Js import VivaGraph_Js


class Test_VivaGraph_Js(Test_Helper):

    def setUp(self):
        super().setUp()
        self.vivagraph = VivaGraph_Js(headless=True)
        #self.result    = None

    #def tearDown(self):
    #    if self.result is not None:
    #        Dev.pprint(self.result)

    def test_create_graph(self):
        (nodes, edges, graph_data, graph_name) = (0,0,0,None)
        Dev.pprint(self.vivagraph.create_graph(nodes, edges))

    def test_create_graph_and_send_screenshot_to_slack(self):
        nodes = [{'key': 'TEAM-23', 'label': 'TEAM-23', 'img_url': 'icons/TEAM.png', 'img_size': 20}]
        edges = []
        png_data = self.vivagraph.create_graph_and_send_screenshot_to_slack(nodes, edges)
        image = (API_Image().load_from_bytes_base64(png_data)
                            .set_img_file('/tmp/temp_image.png')
                            .save())

        # import base64
        # from PIL import Image
        # import io
        self.result = image.info()
        # #self.result = 'asd'

    def test_get_graph_data(self):
        graph_name = 'graph_I3H'
        self.vivagraph.get_graph_data(graph_name)

    # todo: refactor out into new class
    def test_save_jira_icons_locally(self):
        self.result = self.vivagraph.save_jira_icons_locally()


