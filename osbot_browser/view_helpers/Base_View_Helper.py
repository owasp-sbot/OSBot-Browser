from time import sleep

from osbot_aws.apis.Lambda import Lambda
from osbot_aws.apis.S3 import S3

from osbot_browser.browser.API_Browser import API_Browser
from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from osbot_browser.browser.Render_Page import Render_Page
from osbot_browser.browser.Web_Server import Web_Server
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Json import Json


class Base_View_Helpers:
    def __init__(self, web_page,headless=True):
        self.web_page    = web_page
        self.title       = 'browser view'
        self.web_root    = Files.path_combine(Files.parent_folder(__file__), '../web_root')
        self.api_browser = API_Browser(headless=headless).sync__setup_browser()
        self.web_server  = Web_Server(self.web_root)
        self.render_page = Render_Page(api_browser=self.api_browser, web_server=self.web_server)

    # common methods (move to base class)
    def browser(self):
        return self.api_browser

    def browser_width(self,value,height=None):
        self.browser().sync__browser_width(value,height)
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
        data = Lambda('lambdas.gsbot.gsbot_graph').invoke(params)
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

    def assign_variable_js(self, variable, data):
        return self.browser().sync_js_assign_variable(variable,data)

    def set_browser_width_based_on_nodes(self,nodes):
        if   len(nodes) < 30 : self.browser().sync__browser_width(800)
        elif len(nodes) < 100: self.browser().sync__browser_width(1500)
        elif len(nodes) < 200: self.browser().sync__browser_width(2000)
        else                 : self.browser().sync__browser_width(3000)

    def render(self, nodes, edges, js_code=None, options=None, team_id=None, channel=None, sleep_for=None, width=None):
        if len(nodes) > 0:

            if width:
                self.browser().sync__browser_width(width)
            else:
                self.set_browser_width_based_on_nodes(nodes)
                # if          len(nodes) < 50 :                                            sleep_for = 2
                # elif  50 <  len(nodes) < 100: self.browser().sync__browser_width(1000) ; sleep_for = 3
                # elif 100 <  len(nodes) < 200: self.browser().sync__browser_width(2000) ; sleep_for = 5
                # elif        len(nodes) > 200: self.browser().sync__browser_width(3000) ; sleep_for = 10

            self.create_graph(nodes, edges, options)
            self.api_browser.sync__js_execute(js_code)

            if sleep_for: sleep(sleep_for)

            return self.send_screenshot_to_slack(team_id, channel)
            #self.create_graph(nodes, edges,options,graph_name)
            #return self.send_screenshot_to_slack(t§eam_id, channel)
