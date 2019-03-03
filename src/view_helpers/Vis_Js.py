import base64
import json

from browser.API_Browser import API_Browser
from browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
from browser.Render_Page import Render_Page
from utils.Dev import Dev
from utils.Files import Files
from utils.Json import Json
from utils.Local_Cache import use_local_cache_if_available
from utils.aws.Lambdas import Lambdas
from utils.aws.s3 import S3


class Vis_Js:
    def __init__(self, headless=True):
        self.web_page    = '/vis-js/simple.html'
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

    def create_graph_and_send_screenshot_to_slack(self,nodes, edges,options, team_id, channel):
        if len(nodes) >0:
            self.create_graph(nodes, edges,options)
            return self.send_screenshot_to_slack(team_id, channel)

    # Vis js specific

    def add_edge__js_code(self, from_node, to_node):
        edge = {'from': str(from_node), 'to': str(to_node)}
        return 'network.body.data.edges.add({0});'.format(json.dumps(edge))

    def add_edge(self, from_node, to_node):
        self.exec_js(self.add_edge__js_code(from_node,to_node))
        return self

    def add_node__js_code(self, node_id, node_label, shape='box', color=None):
        node = {'id': str(node_id), 'label': str(node_label), 'shape': shape, 'color': color}
        return 'network.body.data.nodes.add({0});'.format(json.dumps(node))

    def add_node(self,node_id, node_label, shape='box',color=None):
        self.exec_js(self.add_node__js_code(node_id, node_label, shape, color))
        return self

    def create_graph(self, nodes = [] ,edges = [],options = None):
        self.load_page(True)
        if options is None or options == {}:
            options = self.get_default_options()

        data = {'nodes': nodes, 'edges': edges}
        base64_data = base64.b64encode(json.dumps(data).encode()).decode()
        base64_options = base64.b64encode(json.dumps(options).encode()).decode()
        js_code = "window.network = new vis.Network(container, JSON.parse(atob('{0}')), JSON.parse(atob('{1}')));".format(base64_data, base64_options)

        #self.browser().sync__browser_width(500, 400)
        self.browser().sync__browser_width(2000)

        self.exec_js(js_code)
        #js_code = [
        #    "network.on('startStabilizing'          , function(data){console.log('startStabilizing', data)})",
        #    "network.on('stabilizationProgress'     , function(data){console.log('stabilizationProgress', data)})",
        #    "network.on('stabilizationIterationsDone', function(data){console.log('stabilizationIterationsDone', data) })",
        #    "network.on('stabilized', function(data) {console.log('stabilized', data) })"]
        #self.exec_js(js_code)

        js_code = "network.on('stabilizationIterationsDone', function(data){ $('body').append('<span id=stabilizationIterationsDone />') })"
        self.exec_js(js_code)
        if self.exec_js("network.physics.ready") is False:
            self.browser().sync__await_for_element('#stabilizationIterationsDone', 20000)
        #self.exec_js("network.on('stabilizationIterationsDone', function(data){console.log('stabilizationIterationsDone', data) })")
        #Dev.print(self.exec_js("network.physics.ready"))
        # need to handle the case when rendering happens very quickly
        #if len(nodes) > 10:


        #js_code = "$('#vis_js').css({ top      : '5px', bottom   : '5px', left     : '5px', right    : '5px', position : 'fixed', border:  '1px solid lightgray'})"
        return self

    def exec_js(self,js_code):
        return self.browser().sync__js_execute(js_code)


    def get_default_options(self):
        options = {
                'nodes'  : { 'font': { 'face' : 'Arial', 'size': 20                       },
                             'shape' : 'box'                                              },
                'edges'  : { 'smooth': False, 'arrows': 'to', 'color': {'color': 'black'}, 'font': { 'size': 10 } },

                'layout' : { 'randomSeed': 0                                              },
                'physics': { 'barnesHut': { 'gravitationalConstant': -700     ,    # (-2000
                                            'centralGravity'       :  0.01    ,    # (0.01) no central gravity since we don't need that
                                            'springLength'         :  50      ,    # (100) this value is also set by the anchor edges
                                            'springConstant'       :  0.0015  ,      # (0.08) this is how hard the spring is
                                            'damping'              :  0.4     ,    # (0.4
                                            'avoidOverlap'         :  0.3                   },
                            'maxVelocity' : 10,                       # (50) keep this low so that the nodes don'y move too far from each other
                            'minVelocity' : 1,                        # (0.1)
                            'solver'      : 'barnesHut',              #       other good option is forceAtlas2Based',
                            'timestep'    : 1.35,                     # (0.5) this value can be used to slow down the animation (for ex 0.015)
                            'stabilization': {
                                'enabled'       : True,
                                'iterations'    : 2000,
                                'updateInterval': 100
                            }

                },
                'interaction': { 'dragNodes': True ,
                                 'zoomView' : True ,
                                 'dragView' : True  } }
        return options

    #@use_local_cache_if_available
    def get_graph_data(self, graph_name):
        params = {'params': ['raw_data', graph_name, 'details'], 'data': {}}
        s3_key = Lambdas('gs.lambda_graph').invoke(params)
        if type(s3_key) is str:
            s3_bucket = 'gs-lambda-tests'
            tmp_file = S3().file_download_and_delete(s3_bucket,s3_key)
            data = Json.load_json_and_delete(tmp_file)
            return data

    def show_jira_graph(self, graph_name, label_key='Summary'):
        self.load_page(False)
        graph_data = self.get_graph_data(graph_name)
        if graph_data:
            nodes = []
            edges = []
            for key, issue in graph_data.get('nodes').items():

                #label = "{0} \n \n{1}".format(issue.get(label_key),issue.get('Labels'))
                label = key
                nodes.append({ 'id' : key , 'label': label})
                #Dev.pprint(issue)

            for edge in graph_data.get('edges'):
                from_node = edge[0]
                link_type = edge[1]
                to_node   = edge[2]
                edges.append({'from' : from_node , 'to': to_node , 'label' : link_type})

            self.create_graph(nodes,edges)

        return graph_data
