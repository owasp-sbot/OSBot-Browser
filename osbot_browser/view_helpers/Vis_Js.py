import base64
import datetime
import json
from time import sleep

from osbot_aws.apis.Lambda import Lambda
from osbot_aws.apis.S3 import S3

from osbot_browser.browser.API_Browser                    import API_Browser
from osbot_browser.browser.Browser_Lamdba_Helper          import Browser_Lamdba_Helper
from osbot_browser.browser.Render_Page                    import Render_Page
from pbx_gs_python_utils.utils.Files        import Files
from pbx_gs_python_utils.utils.Json         import Json



class Vis_Js:
    def __init__(self, headless=True):
        self.web_page    = '/vis-js/simple.html'
        self.web_root    = Files.path_combine(Files.parent_folder(__file__), '../web_root')
        self.api_browser = API_Browser(headless=headless).sync__setup_browser()
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

    # @use_local_cache_if_available
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

    def create_graph(self, nodes = [] ,edges = [],options = None, graph_name=None):

        def show_debug_message(graph_name):
            if graph_name is None:
                graph_name = ''
            today = datetime.date.today().strftime('%d %b %Y')
            self.exec_js("$('#message').html('{0} | {1} nodes {2} edges | created on {3} | by GSBot')".format(graph_name, len(nodes), len(edges), today))

            self.exec_js("$('#status').html('Loading Graph')")

        self.load_page(True)
        if options is None or options == {}:
            options = self.get_default_options()
            #options = self.get_advanced_options()

        data = {'nodes': nodes, 'edges': edges}
        base64_data = base64.b64encode(json.dumps(data).encode()).decode()
        base64_options = base64.b64encode(json.dumps(options).encode()).decode()

        js_code = "window.network = new vis.Network(container, JSON.parse(atob('{0}')), JSON.parse(atob('{1}')));".format(base64_data, base64_options)
        self.exec_js(js_code)

        #self.browser().sync__browser_width(500, 400)
        if len(nodes) > 30:
            self.browser().sync__browser_width(2000)

        show_debug_message(graph_name)

        js_code = "network.on('stabilizationIterationsDone', function(data){ $('body').append('<span style=\"display:none\" id=stabilizationIterationsDone>....done...</span') })"
        self.exec_js(js_code)

        if self.exec_js("network.physics.ready") is False:

            wait_timeout = 10000
            self.browser().sync__await_for_element('#stabilizationIterationsDone', wait_timeout)

            # attempts = 10
            # for i in range(1,attempts):
            #     self.exec_js("$('#status').html('waiting #{0}')".format(i))
            #
            #     #wait_timeout = 1000
            #     result = self.exec_js("$('#stabilizationIterationsDone').html()")
            #     if result == '....done...':
            #         Dev.pprint(">>>> done")
            #         break
            #     #if self.browser().sync__await_for_element('#stabilizationIterationsDone', wait_timeout):
            #     #
            #     #    break
            #     Dev.pprint("attempt: {0}".format(i))
            #     sleep(1)

            self.exec_js('network.stopSimulation()')

        self.exec_js("$('#status').html('')")
                    #break
            #Dev.pprint('dont')
            #

        # js_code = [
        #    "network.on('startStabilizing'          , function(data){console.log('startStabilizing', data)})",
        #    "network.on('stabilizationProgress'     , function(data){console.log('stabilizationProgress', data)})",
        #    "network.on('stabilizationIterationsDone', function(data){console.log('stabilizationIterationsDone', data) })",
        #    "network.on('stabilized', function(data) {console.log('stabilized', data) })"]
        # self.exec_js(js_code)

        #self.exec_js("network.on('stabilizationIterationsDone', function(data){console.log('stabilizationIterationsDone', data) })")
        #Dev.print(self.exec_js("network.physics.ready"))
        # need to handle the case when rendering happens very quickly
        #if len(nodes) > 10:


        #js_code = "$('#vis_js').css({ top      : '5px', bottom   : '5px', left     : '5px', right    : '5px', position : 'fixed', border:  '1px solid lightgray'})"
        return self

    def exec_js(self,js_code):
        return self.browser().sync__js_execute(js_code)

    def invoke_js(self, name, params):
        return self.browser().sync_js_invoke_function(name,params)


    def get_default_options(self):
        return {    'nodes': {'shape': 'box'},
                    'edges': {'arrows': 'to'},
                    'physics': { 'barnesHut': { 'avoidOverlap': 0.1 }, }}

    def get_advanced_options(self):
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

    def wait_n_seconds(self,seconds):
        sleep(seconds)
        return self

    def set_fixed_r1_nodes(self):
        r1s = {
                'RISK-1498': {'x': -1000  , 'y': -1000  },  # 1
                'RISK-1496': {'x':    0   , 'y': -1000  },  # 2
                'RISK-1495': {'x': 1000   , 'y': -1000  }, # 3
                'RISK-1494': {'x': -1000  , 'y':  1000  }, # 4
                'RISK-1534': {'x': 0      , 'y':  1000  }, # 5
                'RISK-1592': {'x': 1000   , 'y':  1000 }} # 6
        for key, value in r1s.items():
            data = {'id': key, 'x':value['x'],'y':value['y'], 'fixed': True, 'mass': 5}
            self.invoke_js('network.body.data.nodes.update', data)

        options = {
            'position': {'x': 0, 'y': 0},
            'offset'  : {'x': 100, 'y': -50},
            'scale'   : 1.0 }

        self.invoke_js('network.moveTo', options)
        return self