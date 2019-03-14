import base64
import datetime
import json
from time import sleep

from browser.API_Browser import API_Browser
from browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from browser.Render_Page import Render_Page
from browser.Web_Server import Web_Server
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
        self.web_server  = Web_Server(self.web_root)
        self.render_page = Render_Page(api_browser=self.api_browser, web_server=self.web_server)



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


    # main methods

    def create_graph(self, nodes, edges, graph_data, graph_name):
        self.web_server.start()
        url = self.web_server.url(self.web_page)

        self.render_page.get_page_html_via_browser(url)

        self.load_page(True)
        layout = {
                    "springLength" : 100,
                    "springCoeff"  : 0.0008,
                    "dragCoeff"    : 0.02,
                    "gravity"      : -10.2
                 };
        self.invoke_js("set_layout",layout)
        js_code = ""
        for key,issue in nodes.items():
            if issue:
                js_code += 'graph.addNode("{0}",{{ "label" : "{1}","img":"{2}"}});'.format(key,key,self.resolve_icon_from_issue_type(issue.get("Issue Type"),key))
        for edge in edges:
            js_code += 'graph.addLink("{0}","{1}");\n'.format(edge[0],edge[2])
            #print(edge)
        # js_code = """graph.addNode("{0}",'icons/vuln.png')
        #              graph.addLink("{0}", "RISK-2");
        #              graph.addLink("RISK-2", "RISK-3");
        #              graph.addLink("RISK-3", "RISK-2");
        #              graph.addLink("RISK-4", "RISK-2");
        #              graph.addLink("RISK-5", "RISK-2");
        #              graph.addLink("RISK-1", "RISK-5");
        #              """.format(graph_name)
        js_code += "run_graph()"
        self.exec_js(js_code)
        self.web_server.stop()
        return 42

    def resolve_icon_from_issue_type(self, issue_type,key):
        mappings = {
            'Risk'           : 'icons/risk_theme.svg',
            'Risk Theme'     : 'icons/risk_theme.svg',
            'Vulnerability'  : 'icons/vuln.png',
            'GS-Project'     : 'icons/gs_project.svg',
            'Business entity': 'icons/business_entity.svg',
            'GS Service '    : 'icons/gs_service.svg',
            'IT Asset'       : 'icons/it_asset.svg',
            'IT System'      : 'icons/it_asset.svg',
            'People'         : 'icons/people.svg',
            'Programme'      : 'icons/programme.svg',
            'Threat Model'   : 'icons/threat_model.svg',
            'Key Result'     : 'icons/key-result.svg',
            'Objective'      : 'icons/objective.svg',
            'Task'           : 'icons/task.svg',
            'Epic'           : 'icons/epic.svg',
            'Data Journey'   : 'icons/data_journey.svg',
            'Project'        : 'icons/project.svg',
            'Fact'           : 'icons/fact.svg',
            'Incident'       : 'icons/incident.png',
            'Incident Task'  : 'icons/incident_task.png',
            'User Access'    : 'icons/user_access.svg',
            'Security Event' : 'icons/security_event.svg',


        }

        icon = mappings.get(issue_type, 'icons/none.jpg')
        if icon is 'icons/none.jpg':
            Dev.pprint(key + ' ' + issue_type)
        return icon

        if issue_type == 'Risk'         : return 'icons/risk_theme.svg'
        if issue_type == 'Risk Theme'   : return 'icons/risk_theme.svg'
        if issue_type == 'Vulnerability': return 'icons/vuln.png'
        #

        Dev.pprint(issue_type)

        return 'icons/none.jpg'