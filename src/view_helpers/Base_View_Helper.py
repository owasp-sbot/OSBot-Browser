from time import sleep

from browser.API_Browser import API_Browser
from browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from browser.Render_Page import Render_Page
from browser.Web_Server import Web_Server
from utils.Files import Files
from utils.Json import Json
from utils.aws.Lambdas import Lambdas
from utils.aws.s3 import S3


class Base_View_Helpers:
    def __init__(self, web_page,headless=True):
        self.web_page    = web_page
        self.title       = 'browser view'
        self.web_root    = Files.path_combine(Files.parent_folder(__file__), '../web_root')
        self.api_browser = API_Browser(headless=headless,auto_close=headless).sync__setup_browser()
        self.web_server  = Web_Server(self.web_root)
        self.render_page = Render_Page(api_browser=self.api_browser, web_server=self.web_server)

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

    def send_screenshot_to_slack(self, team_id=None, channel=None):
        png_file = self.create_dashboard_screenshot()
        return Browser_Lamdba_Helper().send_png_file_to_slack(team_id, channel, self.title, png_file)

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

    def exec_js(self,js_code):
        return self.browser().sync__js_execute(js_code)

    def invoke_js(self, name, params):
        return self.browser().sync_js_invoke_function(name,params)

    def render(self, nodes, edges, js_code=None, options=None, team_id=None, channel=None, use_sleep=False, width=True):
        if len(nodes) > 0:
            sleep_for = 0

            if width:
                self.browser().sync__browser_width(width)
            else:
                if          len(nodes) < 50 :                                            sleep_for = 2
                elif  50 <  len(nodes) < 100: self.browser().sync__browser_width(1000) ; sleep_for = 3
                elif 100 <  len(nodes) < 200: self.browser().sync__browser_width(2000) ; sleep_for = 5
                elif        len(nodes) > 200: self.browser().sync__browser_width(3000) ; sleep_for = 10

            self.create_graph(nodes, edges, options)
            self.api_browser.sync__js_execute(js_code)

            if use_sleep and sleep_for: sleep(sleep_for)
            return self.send_screenshot_to_slack(team_id, channel)
            #self.create_graph(nodes, edges,options,graph_name)
            #return self.send_screenshot_to_slack(t§eam_id, channel)
