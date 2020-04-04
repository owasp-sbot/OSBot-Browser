from time import sleep

from gw_bot.helpers.Lambda_Helpers import slack_message
from osbot_aws.Globals     import Globals
from osbot_aws.apis.Lambda import Lambda
from osbot_aws.apis.S3     import S3

from osbot_browser.browser.API_Browser           import API_Browser
from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
#from osbot_browser.browser.Render_Page           import Render_Page
from osbot_browser.browser.Web_Server            import Web_Server
from osbot_utils.utils.Files                     import path_combine, Files, save_bytes_as_file
from osbot_utils.utils.Json                      import Json
from osbot_utils.utils.Misc                      import json_dumps


class VivaGraph_Js:
    def __init__(self, headless=True):
        self.web_page      = '/vivagraph/simple.html'
        self.jira_icons    = '/vivagraph/icons'
        self.web_root      = path_combine(Files.parent_folder(__file__), '../web_root')
        self.api_browser   = API_Browser(headless=headless).sync__setup_browser()
        self.browser_width = None
        self.render_wait   = None
        self.web_server    = None # Web_Server(self.web_root)
        #self.render_page   = None #Render_Page(api_browser=self.api_browser, web_server=self.web_server)



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
            url = self.web_server.url(self.web_page)
            self.browser().sync__open(url)
            #self.render_page.open_file_in_browser(self.web_page)
        return self

    def create_dashboard_screenshot(self):
        #clip = {'x': 1, 'y': 1, 'width': 945, 'height': 465}
        clip = None
        return self.browser().sync__screenshot(clip=clip)

    def send_screenshot_to_slack(self, team_id, channel):           # todo: refactor screenshot creation from this method
        if self.browser_width:
            self.browser().sync__browser_width(self.browser_width)
        if self.render_wait:
            sleep(self.render_wait)
        png_file = self.create_dashboard_screenshot()
        return Browser_Lamdba_Helper().send_png_file_to_slack(team_id, channel, 'risk dashboard', png_file)

    def get_graph_data(self, graph_name):
        params = {'params': ['raw_data', graph_name, 'details'], 'data': {}}
        data = Lambda('osbot_jira.lambdas.graph').invoke(params)
        if type(data) is str:
            s3_key    = data
            s3_bucket = Globals.lambda_s3_bucket
            tmp_file  = S3().file_download_and_delete(s3_bucket, s3_key)
            data = Json.load_json_and_delete(tmp_file)
            return data
        return data

    def exec_js(self,js_code):
        return self.browser().sync__js_execute(js_code)

    def invoke_js(self, name, params):
        return self.browser().sync_js_invoke_function(name,params)

    def calculate_browser_width_and_wait(self, nodes):
        if self.browser_width is None:
            if         len(nodes) <  20 : self.browser_width = 400
            elif 20  < len(nodes) < 100 : self.browser_width = 1100
            elif 100 < len(nodes) < 300 : self.browser_width = 1500
            else                        : self.browser_width = 3000
        if self.render_wait is None:
            if         len(nodes) < 100 : self.render_wait = 1
            elif 100 < len(nodes) < 300 : self.render_wait = 4
            else                        : self.render_wait = 6
        return self

    #def create_graph_and_send_screenshot_to_slack(self, nodes, edges, options=None, team_id=None, channel=None):
    #    if len(nodes) >0:


    # main methods

    def create_graph(self, nodes, edges,options=None):
        #with  as web_server:
        #self.web_server  = web_server
        #self.render_page =  Render_Page(api_browser=self.api_browser, web_server=self.web_server)
        self.load_page(True)
        layout = {
                    "springLength" : 100,
                    "springCoeff"  : 0.0008,
                    "dragCoeff"    : 0.02,
                    "gravity"      : -10.2
                 };

        self.invoke_js("set_layout",layout)
        js_code = ""

        for node in nodes:
            key       = node.get('key'     )
            label     = node.get('label'   )
            img_url   = node.get('img_url' ) or 'icons/project.svg'
            img_size  = node.get('img_size') or 50
            params = { "label" : label, "img_url": img_url, 'img_size':img_size}
            js_code += 'graph.addNode("{0}",{1});\n'.format(key, json_dumps(params))
        for edge in edges:
            js_code += 'graph.addLink("{0}","{1}");\n'.format(edge[0],edge[2])
        js_code += "run_graph()"

        self.exec_js(js_code)

    def create_graph_and_send_screenshot_to_slack(self, nodes, edges, graph_name=None, screenshot=True, team_id=None, channel=None):
        with Web_Server(self.web_root) as web_server:               # handle server start and stop
            self.web_server = web_server

            self.create_graph(nodes, edges)

            if screenshot:
                self.calculate_browser_width_and_wait(nodes)
                message = f":point_right: Rendering `{graph_name}` using VivaGraph JS engine with: *nodes* `{len(nodes)}` *edges* `{len(edges)}` *width* `{self.browser_width}` and *render_wait* `{self.render_wait}`"
                slack_message(message,[], channel, team_id)
                png_data = self.send_screenshot_to_slack(team_id, channel)
                return png_data
            else:
                return self

    def get_nodes_edges_from_graph_data(self, graph_data):
        edges = graph_data.get('edges')
        nodes = []
        for key, issue in graph_data.get('nodes').items():
            if issue and issue.get("Image"):
                (label, img_size, img_url) = (key, 20, issue.get("Image"))
            else:
                (label, img_size, img_url) = self.resolve_icon_from_key(key)
            node = {
                'key': key,
                'label': label,
                'img_url': img_url,
                'img_size': img_size,
            }
            nodes.append(node)
        return nodes,edges

    def render_gs_graph(self, gs_graph):
        graph_data = gs_graph.get_graph_data()
        (nodes, edges) = self.get_nodes_edges_from_graph_data(graph_data)
        png_data = self.create_graph_and_send_screenshot_to_slack(nodes, edges)
        return png_data

    def resolve_icon_from_key(self, key):       # todo: refactor to use Jira_Icons method
        label    = key
        img_size = 20

        if '-' in key:                          # todo: find better solution to do this
            project_key = key.split('-')[0]
            icon = f'icons/{project_key}.png'
        else:
            icon = 'icons/dot.png'

        return label,img_size,icon


    # todo: refactor this out of this class (since this is the class that is called from the lambda function)
    # see class Jira_Icons
    def save_jira_icons_locally(self):
        from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest
        jira_rest_api = API_Jira_Rest()
        icons = jira_rest_api.projects_icons()
        for key, url in icons.items():
            icon_path  = f'{self.web_root}{self.jira_icons}/{key}.png'
            icon_bytes = jira_rest_api.request_get(url)
            save_bytes_as_file(icon_bytes,icon_path)
        return icons
