import base64
import datetime
import json
from time import sleep

from browser.API_Browser import API_Browser
from browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from browser.Render_Page import Render_Page
from utils.Dev import Dev
from utils.Files import Files
from utils.Json import Json
#from utils.Local_Cache import use_local_cache_if_available
from utils.aws.Lambdas import Lambdas
from utils.aws.s3 import S3


class VivaGraph_Js:
    def __init__(self, headless=True):
        self.web_page    = '/vivagraph/simple.html'
        self.web_root    = Files.path_combine(Files.parent_folder(__file__), '../web_root')
        self.api_browser = API_Browser(headless=headless,auto_close=headless).sync__setup_browser()
        self.render_page = Render_Page(api_browser=self.api_browser, web_root=self.web_root)



        # #self.base_html_file = '/vis-js/empty.html'
        # self.base_html_file = '/vis-js/simple.html'
        # #window.api_visjs
        # self.headless       = False
        # self.browser        = None

    # common methods (move to base class)
    def browser(self):
        return self.api_browser

    def browser_width(self,value):
        self.browser().sync__browser_width(value)
        return self

    def load_page(self,reload=False):
        if reload or self.web_page not in self.browser().sync__url():
            self.render_page.open_file_in_browser(self.web_page)
        return self

    def create_dashboard_screenshot(self):
        #clip = {'x': 1, 'y': 1, 'width': 945, 'height': 465}
        clip = None
        return self.browser().sync__screenshot(clip=clip)

    def send_screenshot_to_slack(self, team_id, channel):
        png_file = self.create_dashboard_screenshot()
        return Browser_Lamdba_Helper().send_png_file_to_slack(team_id, channel, 'risk dashboard', png_file)

    def create_graph_and_send_screenshot_to_slack(self,graph_name, nodes, edges,options, team_id, channel):
        if len(nodes) >0:
            self.create_graph(nodes, edges,options,graph_name)
            return self.send_screenshot_to_slack(team_id, channel)

    #@use_local_cache_if_available
    def get_graph_data(self, graph_name):
        params = {'params': ['raw_data', graph_name, 'details'], 'data': {}}
        data = Lambdas('gsbot.gsbot_graph').invoke(params)
        if type(data) is str:
            s3_key = data
            s3_bucket = 'gs-lambda-tests'
            tmp_file = S3().file_download_and_delete(s3_bucket, s3_key)
            data = Json.load_json_and_delete(tmp_file)
            return data
        return data