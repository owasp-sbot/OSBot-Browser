from time import sleep

from osbot_aws.apis.Lambda import Lambda
from osbot_aws.apis.S3 import S3

from osbot_browser.browser.API_Browser import API_Browser
from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from osbot_browser.browser.Render_Page import Render_Page
from osbot_browser.browser.Web_Server import Web_Server
from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Json import Json
from pbx_gs_python_utils.utils.Misc import Misc



class VivaGraph_Js:
    def __init__(self, headless=True):
        self.web_page    = '/vivagraph/simple.html'
        self.web_root    = Files.path_combine(Files.parent_folder(__file__), '../web_root')
        self.api_browser = API_Browser(headless=headless).sync__setup_browser()
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

    def create_graph_and_send_screenshot_to_slack(self, nodes, edges, options=None, team_id=None, channel=None):
        if len(nodes) >0:
            self.create_graph(nodes, edges,options)
            if          len(nodes) < 20 :                                            sleep(1)
            elif  20 <  len(nodes) < 100: self.browser().sync__browser_width(1500) ; sleep(2)
            elif 100 <  len(nodes) < 200: self.browser().sync__browser_width(2000) ; sleep(5)
            elif        len(nodes) > 200: self.browser().sync__browser_width(3000) ; sleep(10)

            return self.send_screenshot_to_slack(team_id, channel)
            #self.create_graph(nodes, edges,options,graph_name)
            #return self.send_screenshot_to_slack(t§eam_id, channel)


    # main methods

    def create_graph(self, nodes, edges,options=None):
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
        #for key,issue in nodes.items():
        for node in nodes:
            key       = node.get('key'     )
            label     = node.get('label'   )
            img_url   = node.get('img_url' )
            img_size  = node.get('img_size')
            params = { "label" : label, "img_url": img_url, 'img_size':img_size}
            js_code += 'graph.addNode("{0}",{1});'.format(key,Misc.json_dumps(params))
        for edge in edges:
            js_code += 'graph.addLink("{0}","{1}");\n'.format(edge[0],edge[2])
        js_code += "run_graph()"
        self.exec_js(js_code)
        self.web_server.stop()
        return 42

    def resolve_icon_from_issue_type(self, issue,key):
        label    = key
        img_size = 20
        none_icon = 'icons/none.jpg'
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

        if issue and issue.get("Issue Type"):
            issue_type = issue.get("Issue Type")
            icon = mappings.get(issue_type, none_icon)

            #if icon == none_icon:
            #    Dev.pprint(key + ' ' + issue_type)

        else:
            icon = 'icons/none.jpg'
            #icon = 'https://dummyimage.com/100x40/2c2f87/FFFFFF&text={0}'.format(key)
            #img_size = 10

        return label,img_size,icon